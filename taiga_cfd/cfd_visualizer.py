#!/usr/bin/env python3
"""
Taiga CFD Visual Diagram Generator

This module creates beautiful CFD (Cumulative Flow Diagram) visualizations
from CSV data using matplotlib and seaborn.

Features:
- Stacked area charts showing story flow over time
- Status distribution pie charts
- Trend analysis with moving averages
- Professional styling with color schemes
- Multiple export formats (PNG, PDF, SVG)

Usage:
    python3 cfd_visualizer.py [csv_file] [--output-format png]
    python3 cfd_visualizer.py --latest  # Use most recent CSV file
"""

import pandas as pd
# Set matplotlib backend to non-GUI before importing pyplot
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
from datetime import datetime
import os
import sys
import argparse
import json
from pathlib import Path

# Project configuration
PROJECT_SLUG = None  # Will be loaded from config


def load_project_configuration():
    """Load project configuration from config file or environment variables."""
    global PROJECT_SLUG
    
    # First try environment variables
    env_slug = os.getenv("TAIGA_PROJECT_SLUG")
    if env_slug:
        PROJECT_SLUG = env_slug
        return True
    
    # Try to load from project config file
    config_file = Path.cwd() / "project_config.json"
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            PROJECT_SLUG = config_data.get("project_slug", "Project")
            return True
        except Exception:
            pass
    
    # Fallback
    PROJECT_SLUG = "Project"
    return False

# Set style and color palette
plt.style.use("seaborn-v0_8-darkgrid")
sns.set_palette("husl")

# Professional CFD color scheme
CFD_COLORS = {
    "New": "#FF6B6B",  # Coral red - new items
    "Ready": "#4ECDC4",  # Teal - ready to start
    "In progress": "#45B7D1",  # Blue - in progress
    "Code Review": "#96CEB4",  # Mint green - review
    "Deployed on Dev": "#FECA57",  # Yellow - dev environment
    "Deployed on QA": "#FF9FF3",  # Pink - QA environment
    "In QA": "#54A0FF",  # Light blue - testing
    "QA Bugs": "#FF6348",  # Red - bugs found
    "QA Verified": "#2ED573",  # Green - verified
    "Deployed on Stage": "#FFA502",  # Orange - staging
    "Ready for Deployment": "#3742FA",  # Purple - ready to deploy
    "Done": "#2F3542",  # Dark gray - completed
    "On Hold": "#A4B0BE",  # Gray - on hold
    "Needs Info": "#F1C40F",  # Gold - needs information
    "Archived": "#95A5A6",  # Light gray - archived
}


def load_cfd_data(csv_file):
    """Load CFD data from CSV file."""
    try:
        df = pd.read_csv(csv_file)
        df["date"] = pd.to_datetime(df["date"])
        return df
    except Exception as e:
        print(f"❌ Error loading CSV file: {e}")
        return None


def find_latest_csv():
    """Find the most recent CFD CSV file."""
    data_dir = Path.cwd()
    cfd_files = list(data_dir.glob("cfd_data_*.csv"))
    if not cfd_files:
        print("❌ No CFD CSV files found in current directory")
        return None

    # Sort by modification time
    latest_file = max(cfd_files, key=lambda f: f.stat().st_mtime)
    print(f"📊 Using latest CFD file: {latest_file.name}")
    return str(latest_file)


def create_cfd_stacked_area(df, output_file=None):
    """Create a stacked area chart for CFD visualization."""
    print("📈 Creating CFD stacked area chart...")

    # Prepare data for stacking
    status_columns = [col for col in df.columns if col not in ["date", "total"]]

    # Create figure with professional styling
    fig, ax = plt.subplots(figsize=(14, 8))

    # Create stacked area plot
    colors = [
        CFD_COLORS.get(status, sns.color_palette("husl", len(status_columns))[i])
        for i, status in enumerate(status_columns)
    ]

    ax.stackplot(
        df["date"],
        *[df[col] for col in status_columns],
        labels=status_columns,
        colors=colors,
        alpha=0.8,
    )

    # Styling
    ax.set_title(
        "📈 Cumulative Flow Diagram (CFD)\nDaily Story Count by Status",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )
    ax.set_xlabel("Date", fontsize=12, fontweight="bold")
    ax.set_ylabel("Story Count", fontsize=12, fontweight="bold")

    # Format x-axis dates
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
    ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))

    # Rotate date labels
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")

    # Legend with better positioning
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=10)

    # Grid styling
    ax.grid(True, alpha=0.3)
    ax.set_facecolor("#f8f9fa")

    # Add summary statistics
    total_stories = df["total"].iloc[-1]
    date_range = f"{df['date'].iloc[0].strftime('%m/%d/%Y')} - {df['date'].iloc[-1].strftime('%m/%d/%Y')}"

    ax.text(
        0.02,
        0.98,
        f"Total Stories: {total_stories}\nDate Range: {date_range}",
        transform=ax.transAxes,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
        fontsize=10,
    )

    plt.tight_layout()

    # Save the plot
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches="tight", facecolor="white")
        print(f"✅ CFD stacked area chart saved to: {output_file}")

    return fig


def create_status_distribution_pie(df, output_file=None):
    """Create a pie chart showing current status distribution."""
    print("🥧 Creating status distribution pie chart...")

    # Get latest data point
    latest_data = df.iloc[-1]
    status_columns = [col for col in df.columns if col not in ["date", "total"]]

    # Filter out zero values
    status_counts = {
        col: latest_data[col] for col in status_columns if latest_data[col] > 0
    }

    fig, ax = plt.subplots(figsize=(10, 8))

    # Create pie chart
    colors = [
        CFD_COLORS.get(status, sns.color_palette("husl", len(status_counts))[i])
        for i, status in enumerate(status_counts.keys())
    ]

    wedges, texts, autotexts = ax.pie(
        status_counts.values(),
        labels=status_counts.keys(),
        colors=colors,
        autopct="%1.1f%%",
        startangle=90,
        explode=[0.05 if status == "Done" else 0 for status in status_counts.keys()],
    )

    # Styling
    ax.set_title(
        "📊 Current Status Distribution\n(Latest CFD Data Point)",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )

    # Make percentage text more readable
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontweight("bold")
        autotext.set_fontsize(10)

    # Add total count
    total = sum(status_counts.values())
    ax.text(
        0,
        -1.3,
        f"Total Stories: {total}",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
    )

    plt.tight_layout()

    # Save the plot
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches="tight", facecolor="white")
        print(f"✅ Status distribution pie chart saved to: {output_file}")

    return fig


def create_trend_analysis(df, output_file=None):
    """Create trend analysis with moving averages."""
    print("📈 Creating trend analysis chart...")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    # Top chart: Total stories over time with moving average
    ax1.plot(
        df["date"],
        df["total"],
        "o-",
        linewidth=2,
        markersize=4,
        color="#2E86AB",
        label="Daily Total",
        alpha=0.7,
    )

    # 7-day moving average
    if len(df) >= 7:
        df["7day_avg"] = df["total"].rolling(window=7, center=True).mean()
        ax1.plot(
            df["date"],
            df["7day_avg"],
            "--",
            linewidth=3,
            color="#A23B72",
            label="7-Day Moving Average",
        )

    ax1.set_title("📈 Story Count Trend Analysis", fontsize=14, fontweight="bold")
    ax1.set_xlabel("Date", fontsize=12)
    ax1.set_ylabel("Total Stories", fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Bottom chart: Daily velocity (story additions)
    df["daily_change"] = df["total"].diff().fillna(0)

    # Color bars based on positive/negative change
    colors = ["#2ED573" if x >= 0 else "#FF6B6B" for x in df["daily_change"]]
    ax2.bar(df["date"], df["daily_change"], color=colors, alpha=0.7, width=0.8)

    ax2.set_title(
        "📊 Daily Story Velocity (Net Changes)", fontsize=14, fontweight="bold"
    )
    ax2.set_xlabel("Date", fontsize=12)
    ax2.set_ylabel("Stories Added/Removed", fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color="black", linestyle="-", alpha=0.3)

    # Format x-axis for both subplots
    for ax in [ax1, ax2]:
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")

    plt.tight_layout()

    # Save the plot
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches="tight", facecolor="white")
        print(f"✅ Trend analysis chart saved to: {output_file}")

    return fig


def create_comprehensive_dashboard(df, output_file=None):
    """Create a comprehensive CFD dashboard with multiple visualizations."""
    print("🎯 Creating comprehensive CFD dashboard...")

    fig = plt.figure(figsize=(20, 12))

    # Create grid layout
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

    # 1. Main CFD stacked area (spans 2x2)
    ax1 = fig.add_subplot(gs[0:2, 0:2])

    status_columns = [col for col in df.columns if col not in ["date", "total"]]
    colors = [
        CFD_COLORS.get(status, sns.color_palette("husl", len(status_columns))[i])
        for i, status in enumerate(status_columns)
    ]

    ax1.stackplot(
        df["date"],
        *[df[col] for col in status_columns],
        labels=status_columns,
        colors=colors,
        alpha=0.8,
    )

    ax1.set_title("📈 Cumulative Flow Diagram", fontsize=14, fontweight="bold")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Story Count")
    ax1.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)
    ax1.grid(True, alpha=0.3)

    # 2. Status distribution pie chart
    ax2 = fig.add_subplot(gs[0, 2])
    latest_data = df.iloc[-1]
    status_counts = {
        col: latest_data[col] for col in status_columns if latest_data[col] > 0
    }

    pie_colors = [
        CFD_COLORS.get(status, sns.color_palette("husl", len(status_counts))[i])
        for i, status in enumerate(status_counts.keys())
    ]

    ax2.pie(
        status_counts.values(),
        labels=status_counts.keys(),
        colors=pie_colors,
        autopct="%1.0f%%",
        textprops={"fontsize": 8},
    )
    ax2.set_title("📊 Current Distribution", fontsize=10, fontweight="bold")

    # 3. Trend line
    ax3 = fig.add_subplot(gs[1, 2])
    ax3.plot(df["date"], df["total"], "o-", linewidth=2, markersize=3, color="#2E86AB")
    ax3.set_title("📈 Total Trend", fontsize=10, fontweight="bold")
    ax3.tick_params(axis="x", rotation=45, labelsize=8)
    ax3.grid(True, alpha=0.3)

    # 4. Daily velocity bar chart
    ax4 = fig.add_subplot(gs[2, :])
    df["daily_change"] = df["total"].diff().fillna(0)
    colors = ["#2ED573" if x >= 0 else "#FF6B6B" for x in df["daily_change"]]

    ax4.bar(df["date"], df["daily_change"], color=colors, alpha=0.7, width=0.8)
    ax4.set_title("📊 Daily Story Velocity", fontsize=12, fontweight="bold")
    ax4.set_xlabel("Date")
    ax4.set_ylabel("Net Story Changes")
    ax4.axhline(y=0, color="black", linestyle="-", alpha=0.3)
    ax4.grid(True, alpha=0.3)
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha="right")

    # Add overall title and metadata
    load_project_configuration()  # Ensure config is loaded
    fig.suptitle(
        f"📊 Taiga CFD Analytics Dashboard - {PROJECT_SLUG}",
        fontsize=18,
        fontweight="bold",
        y=0.98,
    )

    total_stories = df["total"].iloc[-1]
    date_range = f"{df['date'].iloc[0].strftime('%m/%d/%Y')} - {df['date'].iloc[-1].strftime('%m/%d/%Y')}"

    fig.text(
        0.02,
        0.02,
        f"📈 Total Stories: {total_stories} | 📅 Period: {date_range} | 📊 Data Points: {len(df)}",
        fontsize=12,
        bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.5),
    )

    # Save the dashboard
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches="tight", facecolor="white")
        print(f"✅ Comprehensive CFD dashboard saved to: {output_file}")

    return fig


def generate_all_visualizations(csv_file, output_format="png"):
    """Generate all CFD visualizations from a CSV file."""
    print("🎨 TAIGA CFD VISUALIZATION GENERATOR")
    print("=" * 50)

    # Load data
    df = load_cfd_data(csv_file)
    if df is None:
        return False

    print(f"📊 Loaded {len(df)} data points from {csv_file}")
    print(
        f"📅 Date range: {df['date'].iloc[0].strftime('%Y-%m-%d')} to {df['date'].iloc[-1].strftime('%Y-%m-%d')}"
    )
    print()

    # Generate base filename
    base_name = Path(csv_file).stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create output directory
    output_dir = Path.cwd() / "cfd_visualizations"
    output_dir.mkdir(exist_ok=True)

    try:
        # 1. Comprehensive Dashboard
        dashboard_file = (
            output_dir / f"{base_name}_dashboard_{timestamp}.{output_format}"
        )
        create_comprehensive_dashboard(df, dashboard_file)

        # 2. Stacked Area Chart
        area_file = output_dir / f"{base_name}_stackedarea_{timestamp}.{output_format}"
        create_cfd_stacked_area(df, area_file)

        # 3. Status Distribution Pie Chart
        pie_file = output_dir / f"{base_name}_distribution_{timestamp}.{output_format}"
        create_status_distribution_pie(df, pie_file)

        # 4. Trend Analysis
        trend_file = output_dir / f"{base_name}_trends_{timestamp}.{output_format}"
        create_trend_analysis(df, trend_file)

        print(f"\n✅ All visualizations generated successfully!")
        print(f"📁 Output directory: {output_dir}")
        print(f"📊 Charts created:")
        print(f"   • Dashboard: {dashboard_file.name}")
        print(f"   • Stacked Area: {area_file.name}")
        print(f"   • Distribution: {pie_file.name}")
        print(f"   • Trends: {trend_file.name}")

        return True

    except Exception as e:
        print(f"❌ Error generating visualizations: {e}")
        return False

    finally:
        plt.close("all")  # Clean up matplotlib figures


def main():
    """Main visualization function."""
    # Load project configuration
    load_project_configuration()
    
    parser = argparse.ArgumentParser(description="Generate CFD visualizations")
    parser.add_argument("csv_file", nargs="?", help="CSV file path")
    parser.add_argument("--latest", action="store_true", help="Use latest CSV file")
    parser.add_argument(
        "--output-format",
        choices=["png", "pdf", "svg"],
        default="png",
        help="Output format for charts",
    )

    args = parser.parse_args()

    # Determine CSV file to use
    if args.latest:
        csv_file = find_latest_csv()
        if not csv_file:
            sys.exit(1)
    elif args.csv_file:
        csv_file = args.csv_file
        if not os.path.exists(csv_file):
            print(f"❌ CSV file not found: {csv_file}")
            sys.exit(1)
    else:
        print("❌ Please specify a CSV file or use --latest flag")
        sys.exit(1)

    # Generate visualizations
    success = generate_all_visualizations(csv_file, args.output_format)

    if success:
        print(f"\n🎉 CFD visualizations are ready!")
        print(f"💡 Open the charts to analyze your team's workflow patterns")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
