#!/usr/bin/env python3
"""
Taiga CFD (Cumulative Flow Diagram) Generator

This script generates CFD data for the azeb-admin-empathy project,
providing insights into team progress and workflow efficiency.

Usage:
    python3 taiga_cfd_generator.py [options]

Options:
    --months=N                Number of months to analyze (default: 6)
    --granularity=LEVEL      Data granularity: daily, weekly, monthly (default: daily)
    --start-date=YYYY-MM-DD  Custom start date
    --end-date=YYYY-MM-DD    Custom end date

Examples:
    python3 taiga_cfd_generator.py --months=3 --granularity=daily
    python3 taiga_cfd_generator.py --start-date=2025-01-01 --end-date=2025-03-31 --granularity=weekly
"""

import json
import requests
import sys
import os
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import csv
from pathlib import Path

# Configuration - Load from project config file or environment variables
TAIGA_API_BASE_URL = os.getenv("TAIGA_API_BASE_URL", "https://api.taiga.io")
PROJECT_SLUG = None  # Will be loaded from config
PROJECT_ID = None    # Will be loaded from config


def load_project_configuration():
    """Load project configuration from config file or environment variables."""
    global PROJECT_SLUG, PROJECT_ID
    
    # First try environment variables
    env_slug = os.getenv("TAIGA_PROJECT_SLUG")
    env_id = os.getenv("TAIGA_PROJECT_ID")
    
    if env_slug and env_id:
        try:
            PROJECT_SLUG = env_slug
            PROJECT_ID = int(env_id)
            print(f"✅ Using project from environment: {PROJECT_SLUG} (ID: {PROJECT_ID})")
            return True
        except ValueError:
            print("⚠️  Invalid TAIGA_PROJECT_ID in environment (must be integer)")
    
    # Try to load from project config file
    config_file = Path.cwd() / "project_config.json"
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            PROJECT_SLUG = config_data.get("project_slug")
            PROJECT_ID = config_data.get("project_id")
            
            if PROJECT_SLUG and PROJECT_ID:
                print(f"✅ Loaded project configuration: {PROJECT_SLUG} (ID: {PROJECT_ID})")
                return True
        except Exception as e:
            print(f"⚠️  Could not load project configuration: {e}")
    
    # Fallback to old defaults if nothing else works
    PROJECT_SLUG = "your-project-slug"
    PROJECT_ID = 0
    print("⚠️  Using fallback project configuration")
    return False


def load_tokens_from_file(filename):
    """Load authentication tokens from a JSON file."""
    try:
        if not os.path.exists(filename):
            print(f"❌ Token file not found: {filename}")
            return None

        with open(filename, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load tokens: {e}")
        return None


def make_api_request(endpoint, auth_token, params=None, method="GET"):
    """Make an authenticated API request."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}",
    }

    url = f"{TAIGA_API_BASE_URL}{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params, timeout=30)
        else:
            response = requests.request(
                method, url, headers=headers, params=params, timeout=30
            )
        return response
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None


def verify_project_access(auth_token):
    """Verify we can access the target project."""
    print(f"🔍 Verifying access to project: {PROJECT_SLUG}")

    params = {"slug": PROJECT_SLUG}
    response = make_api_request("/api/v1/projects/by_slug", auth_token, params)

    if response and response.status_code == 200:
        project = response.json()
        print(f"✅ Project access verified: {project['name']}")
        print(f"   ID: {project['id']}")
        print(f"   Is Private: {project.get('is_private', False)}")
        print(f"   Permissions: {len(project.get('my_permissions', []))}")
        print(f"   Is Kanban Active: {project.get('is_kanban_activated', False)}")
        return project
    else:
        print(
            f"❌ Cannot access project: {response.status_code if response else 'No response'}"
        )
        return None


def get_project_user_stories(auth_token, project_id, months_back=6):
    """Get all user stories for the project within the time range."""
    print(
        f"📊 Fetching user stories for project {project_id} (last {months_back} months)"
    )

    # Calculate date range with timezone awareness
    from datetime import timezone

    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=months_back * 30)

    print(
        f"   Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
    )

    all_stories = []
    page = 1

    while True:
        params = {"project": project_id, "page": page, "page_size": 100}

        print(f"   📄 Fetching user stories page {page}...")
        response = make_api_request("/api/v1/userstories", auth_token, params)

        if not response or response.status_code != 200:
            print(
                f"❌ Failed to fetch user stories page {page}: {response.status_code if response else 'No response'}"
            )
            break

        stories = response.json()

        if not stories:
            print(f"✅ No more user stories on page {page}")
            break

        # Filter by date range
        filtered_stories = []
        for story in stories:
            try:
                created_date_str = story["created_date"]
                # Handle both Z and timezone offset formats
                if created_date_str.endswith("Z"):
                    created_date = datetime.fromisoformat(
                        created_date_str.replace("Z", "+00:00")
                    )
                else:
                    created_date = datetime.fromisoformat(created_date_str)

                # Make sure created_date is timezone-aware
                if created_date.tzinfo is None:
                    created_date = created_date.replace(tzinfo=timezone.utc)

                if created_date >= start_date:
                    filtered_stories.append(story)
            except (ValueError, KeyError) as e:
                print(f"   ⚠️ Skipping story due to date parsing error: {e}")
                continue

        all_stories.extend(filtered_stories)
        print(
            f"   Found {len(filtered_stories)} stories in date range on page {page} (total: {len(stories)})"
        )

        # If we have fewer stories than page_size, we've reached the end
        if len(stories) < 100:
            break

        page += 1

        # Safety check
        if page > 20:
            print("⚠️ Reached page limit (20), stopping")
            break

    print(f"📊 Total user stories in range: {len(all_stories)}")
    return all_stories


def get_project_statuses(auth_token, project_id):
    """Get all user story statuses for the project."""
    print(f"📊 Fetching user story statuses for project {project_id}")

    params = {"project": project_id}
    response = make_api_request("/api/v1/userstory-statuses", auth_token, params)

    if response and response.status_code == 200:
        statuses = response.json()
        print(f"✅ Found {len(statuses)} user story statuses")

        for status in statuses:
            print(
                f"   • {status['name']} (ID: {status['id']}, Closed: {status.get('is_closed', False)})"
            )

        return statuses
    else:
        print(
            f"❌ Failed to get statuses: {response.status_code if response else 'No response'}"
        )
        if response and response.text:
            print(f"   Error: {response.text[:200]}")
        return []


def get_story_history(auth_token, story_id):
    """Get the history of status changes for a user story."""
    response = make_api_request(f"/api/v1/history/userstory/{story_id}", auth_token)

    if response and response.status_code == 200:
        history = response.json()
        return history
    else:
        return []


def generate_cfd_data(
    stories,
    statuses,
    months_back=6,
    granularity="daily",
    start_date=None,
    end_date=None,
):
    """Generate CFD data from user stories and their status changes with configurable granularity.

    Args:
        stories: List of user stories
        statuses: List of status objects
        months_back: Number of months to look back (used if start_date/end_date not provided)
        granularity: 'daily', 'weekly', or 'monthly'
        start_date: Custom start date (timezone-aware datetime)
        end_date: Custom end date (timezone-aware datetime)
    """
    print(f"📈 Generating {granularity} CFD data...")

    # Create status lookup
    status_lookup = {s["id"]: s["name"] for s in statuses}

    # Determine date range with timezone awareness
    from datetime import timezone

    if start_date and end_date:
        # Use provided custom dates
        analysis_start = start_date
        analysis_end = end_date
        print(
            f"   📅 Using custom date range: {analysis_start.strftime('%Y-%m-%d')} to {analysis_end.strftime('%Y-%m-%d')}"
        )
    else:
        # Use months_back calculation
        analysis_end = datetime.now(timezone.utc)
        analysis_start = analysis_end - timedelta(days=months_back * 30)
        print(
            f"   📅 Using {months_back} months back: {analysis_start.strftime('%Y-%m-%d')} to {analysis_end.strftime('%Y-%m-%d')}"
        )

    # Determine time delta based on granularity
    if granularity == "daily":
        time_delta = timedelta(days=1)
        print(f"   📊 Granularity: Daily data points")
    elif granularity == "weekly":
        time_delta = timedelta(days=7)
        print(f"   📊 Granularity: Weekly data points")
    elif granularity == "monthly":
        time_delta = timedelta(days=30)  # Approximate monthly
        print(f"   📊 Granularity: Monthly data points")
    else:
        time_delta = timedelta(days=1)  # Default to daily
        print(f"   ⚠️  Unknown granularity '{granularity}', defaulting to daily")

    # Generate data points for CFD
    current_date = analysis_start
    cfd_data = []

    print(f"   📅 Generating {granularity} CFD data points...")

    while current_date <= analysis_end:
        daily_counts = Counter()

        for story in stories:
            try:
                created_date_str = story["created_date"]
                # Handle both Z and timezone offset formats
                if created_date_str.endswith("Z"):
                    story_created = datetime.fromisoformat(
                        created_date_str.replace("Z", "+00:00")
                    )
                else:
                    story_created = datetime.fromisoformat(created_date_str)

                # Make sure story_created is timezone-aware
                if story_created.tzinfo is None:
                    story_created = story_created.replace(tzinfo=timezone.utc)

                # Only count stories that existed on this date
                if story_created <= current_date:
                    status_id = story["status"]
                    status_name = status_lookup.get(status_id, f"Status {status_id}")
                    daily_counts[status_name] += 1
            except (ValueError, KeyError) as e:
                continue  # Skip problematic stories

        cfd_data.append(
            {
                "date": current_date.strftime("%Y-%m-%d"),
                "counts": dict(daily_counts),
                "total": sum(daily_counts.values()),
            }
        )

        current_date += time_delta

    print(f"✅ Generated {len(cfd_data)} {granularity} data points")

    # Show data density info
    if cfd_data:
        total_points = len(cfd_data)
        date_range_days = (analysis_end - analysis_start).days
        coverage_desc = {
            "daily": f"{total_points} days (~{total_points/30.44:.1f} months)",
            "weekly": f"{total_points} weeks (~{total_points/4.33:.1f} months)",
            "monthly": f"{total_points} months",
        }

        print(
            f"   📊 Coverage: {coverage_desc.get(granularity, str(total_points))} of data"
        )
        print(f"   📈 Granularity: {granularity.title()} CFD measurements")

    return cfd_data


def save_cfd_to_csv(cfd_data, filename):
    """Save CFD data to CSV file."""
    if not cfd_data:
        print("❌ No CFD data to save")
        return

    # Get all unique statuses across all data points
    all_statuses = set()
    for data_point in cfd_data:
        all_statuses.update(data_point["counts"].keys())

    all_statuses = sorted(list(all_statuses))

    print(f"💾 Saving CFD data to {filename}")
    print(f"   Statuses: {', '.join(all_statuses)}")

    with open(filename, "w", newline="") as csvfile:
        # Prepare headers
        headers = ["date", "total"] + all_statuses
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        # Write data
        for data_point in cfd_data:
            row = {"date": data_point["date"], "total": data_point["total"]}

            # Add status counts
            for status in all_statuses:
                row[status] = data_point["counts"].get(status, 0)

            writer.writerow(row)

    print(f"✅ CFD data saved to {filename}")
    print(f"   📊 {len(cfd_data)} daily data points exported")
    print(f"   📅 Date range: {cfd_data[0]['date']} to {cfd_data[-1]['date']}")


def print_cfd_summary(cfd_data, statuses):
    """Print a summary of the CFD data."""
    if not cfd_data:
        return

    print("\n" + "=" * 50)
    print("📈 CFD SUMMARY")
    print("=" * 50)

    first_point = cfd_data[0]
    last_point = cfd_data[-1]

    print(f"📅 Date Range: {first_point['date']} to {last_point['date']}")
    print(f"📊 Total Data Points: {len(cfd_data)}")

    print(f"\n📈 Story Count Evolution:")
    print(f"   Start: {first_point['total']} stories")
    print(f"   End: {last_point['total']} stories")
    print(f"   Growth: {last_point['total'] - first_point['total']} stories")

    # Status breakdown for latest point
    print(f"\n📋 Current Status Distribution:")
    for status_name, count in sorted(last_point["counts"].items()):
        percentage = (
            (count / last_point["total"] * 100) if last_point["total"] > 0 else 0
        )
        print(f"   • {status_name}: {count} ({percentage:.1f}%)")


def main():
    """Main CFD generation function."""
    # Load project configuration first
    config_loaded = load_project_configuration()
    if not config_loaded:
        print("⚠️  Using fallback project configuration")
    
    print("=" * 70)
    print("📈 TAIGA CFD GENERATOR")
    print("=" * 70)
    print(f"🎯 Target Project: {PROJECT_SLUG} (ID: {PROJECT_ID})")
    
    # Validate project configuration
    if not PROJECT_SLUG or PROJECT_SLUG == "your-project-slug" or not PROJECT_ID or PROJECT_ID == 0:
        print("\n❌ Invalid project configuration!")
        print("💡 Please run the CLI interface first to configure your project:")
        print("   python3 -m taiga_cfd.cli")
        print("   or set environment variables:")
        print("   export TAIGA_PROJECT_SLUG='your-actual-project-slug'")
        print("   export TAIGA_PROJECT_ID='your-actual-project-id'")
        sys.exit(1)
    
    print()

    # Parse command line arguments for advanced options
    months_back = 6
    granularity = "daily"
    custom_start_date = None
    custom_end_date = None

    if len(sys.argv) > 1:
        i = 1
        while i < len(sys.argv):
            arg = sys.argv[i]

            if arg.startswith("--months="):
                try:
                    months_back = int(arg.split("=")[1])
                except ValueError:
                    print("⚠️ Invalid months parameter, using default: 6 months")

            elif arg.startswith("--granularity="):
                granularity = arg.split("=")[1]
                if granularity not in ["daily", "weekly", "monthly"]:
                    print("⚠️ Invalid granularity, using default: daily")
                    granularity = "daily"

            elif arg.startswith("--start-date="):
                try:
                    from datetime import timezone

                    date_str = arg.split("=")[1]
                    custom_start_date = datetime.strptime(date_str, "%Y-%m-%d").replace(
                        tzinfo=timezone.utc
                    )
                except ValueError:
                    print("⚠️ Invalid start date format, expected YYYY-MM-DD")

            elif arg.startswith("--end-date="):
                try:
                    from datetime import timezone

                    date_str = arg.split("=")[1]
                    custom_end_date = datetime.strptime(date_str, "%Y-%m-%d").replace(
                        tzinfo=timezone.utc
                    )
                except ValueError:
                    print("⚠️ Invalid end date format, expected YYYY-MM-DD")

            elif arg == "--months" and i + 1 < len(sys.argv):
                try:
                    months_back = int(sys.argv[i + 1])
                    i += 1  # Skip next argument as it's the value
                except ValueError:
                    print("⚠️ Invalid months parameter, using default: 6 months")

            i += 1

    # Validate custom date range
    if custom_start_date and custom_end_date:
        if custom_end_date < custom_start_date:
            print("⚠️ End date must be after start date, using default range")
            custom_start_date = None
            custom_end_date = None

    # Show configuration
    if custom_start_date and custom_end_date:
        print(
            f"📅 Analysis period: {custom_start_date.strftime('%Y-%m-%d')} to {custom_end_date.strftime('%Y-%m-%d')}"
        )
    else:
        print(f"📅 Analysis period: Last {months_back} months")

    print(f"📊 Data granularity: {granularity.title()}")
    print()

    # Load token
    data_dir = Path.cwd()
    token_files = list(data_dir.glob("taiga_tokens_*.json"))
    if not token_files:
        print("❌ No token file found. Please run taiga-cfd first to authenticate.")
        sys.exit(1)

    token_file = max(token_files, key=lambda f: f.stat().st_mtime)
    token_data = load_tokens_from_file(str(token_file))

    if not token_data:
        sys.exit(1)

    auth_token = token_data.get("auth_token")
    user_info = token_data.get("user_info", {})

    print(f"👤 User: {user_info.get('full_name', 'Unknown')}")
    print(f"🔑 Token file: {token_file}")
    print()

    # Step 1: Verify project access
    project = verify_project_access(auth_token)
    if not project:
        sys.exit(1)

    print()

    # Step 2: Get project statuses
    statuses = get_project_statuses(auth_token, PROJECT_ID)
    if not statuses:
        print("❌ Cannot proceed without status information")
        sys.exit(1)

    print()

    # Step 3: Get user stories
    stories = get_project_user_stories(auth_token, PROJECT_ID, months_back)
    if not stories:
        print("❌ No user stories found in the specified time range")
        sys.exit(1)

    print()

    # Step 4: Generate CFD data with custom parameters
    cfd_data = generate_cfd_data(
        stories, statuses, months_back, granularity, custom_start_date, custom_end_date
    )

    # Step 5: Save to CSV with granularity indicator
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"cfd_data_{PROJECT_SLUG}_{granularity}_{timestamp}.csv"
    save_cfd_to_csv(cfd_data, csv_filename)

    # Step 6: Print summary
    print_cfd_summary(cfd_data, statuses)

    # Step 7: Generate visualizations
    try:
        print(f"\n🎨 Generating CFD visualizations...")
        
        # Import visualizer module - handle both package and direct execution
        try:
            from . import cfd_visualizer
        except ImportError:
            # Fallback for when running as standalone script
            import cfd_visualizer
        
        # Set up arguments for the visualizer
        original_argv = sys.argv
        sys.argv = ['cfd_visualizer', csv_filename]
        
        try:
            cfd_visualizer.main()
            visualization_success = True
        except SystemExit as e:
            visualization_success = e.code == 0
        except Exception:
            visualization_success = False
        finally:
            sys.argv = original_argv

        if visualization_success:
            print(f"✅ Visual CFD charts created in cfd_visualizations/ directory")
        else:
            print(f"⚠️ Visualization generation failed - CSV data still available")
    except ImportError as e:
        print(f"⚠️ Visualization libraries not available: {e}")
        print(f"💡 Install with: pip install matplotlib seaborn pandas")
    except Exception as e:
        print(f"⚠️ Visualization generation failed: {e}")

    print(f"\n✅ CFD Generation Complete!")
    print(f"📄 Data saved to: {csv_filename}")
    print(f"🎨 Visual charts: Check cfd_visualizations/ directory")
    print(f"💡 You can also import CSV into Excel or your preferred charting tool")
    print(
        f"📈 Create a stacked area chart with dates on X-axis and status counts on Y-axis"
    )
    print(f"🗓️ Each row represents one day - perfect for daily CFD insights!")


if __name__ == "__main__":
    main()
