#!/usr/bin/env python3
"""
Setup script for Taiga CFD Analytics System - GitHub Ready Edition
Professional pip package for enterprise users with modern TUI interface

This setup.py is synchronized with the taiga_cfd module structure
and is designed for GitHub distribution and PyPI publishing.
"""

from setuptools import setup, find_packages
from pathlib import Path
import os

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


# Version - synchronized with taiga_cfd module
# Read version from the module's __init__.py file
def get_version():
    """Get version from package __init__.py"""
    try:
        with open("taiga_cfd/__init__.py", "r") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"')
    except Exception:
        pass
    return "2.3.2"  # Fallback


__version__ = get_version()

setup(
    name="taiga-cfd-analytics",
    version=__version__,
    author="Muhammad Zeshan Ayub",
    author_email="zeshanayub.connect@gmail.com",
    description="Enterprise-grade Cumulative Flow Diagram (CFD) analytics system for Taiga project management with modern Terminal User Interface (TUI)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ydrgzm/taiga-cfd-analytics",
    project_urls={
        "Bug Tracker": "https://github.com/ydrgzm/taiga-cfd-analytics/issues",
        "Documentation": "https://github.com/ydrgzm/taiga-cfd-analytics#readme",
        "Source Code": "https://github.com/ydrgzm/taiga-cfd-analytics",
        "Funding": "https://github.com/sponsors/ydrgzm",
    },
    packages=find_packages(include=["taiga_cfd", "taiga_cfd.*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial :: Spreadsheet",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
        "Environment :: Console :: Curses",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.1",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "rich>=13.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "taiga-cfd=taiga_cfd.cli:main",
            "taiga-cfd-analytics=taiga_cfd.cli:main",
            "taiga-analytics=taiga_cfd.cli:main",
            "taiga-cfd-generator=taiga_cfd.taiga_cfd_generator:main",
            "taiga-cfd-visualizer=taiga_cfd.cfd_visualizer:main",
        ],
    },
    include_package_data=True,
    package_data={
        "taiga_cfd": ["*.md", "*.txt", "*.json", "*.cfg"],
        "": ["*.md", "*.txt", "*.rst", "LICENSE"],
    },
    data_files=[
        (
            "share/taiga-cfd-analytics",
            ["README.md", "LICENSE", "CHANGELOG.md", "CONTRIBUTING.md"],
        ),
    ],
    keywords=[
        "taiga",
        "cfd",
        "cumulative-flow-diagram",
        "analytics",
        "project-management",
        "kanban",
        "agile",
        "visualization",
        "reporting",
        "enterprise",
        "tui",
        "terminal",
        "dashboard",
        "metrics",
        "scrum",
        "devops",
    ],
    zip_safe=False,
)
