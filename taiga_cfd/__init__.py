#!/usr/bin/env python3
"""
Taiga CFD Analytics - Enterprise Terminal Interface

A comprehensive tool for generating Cumulative Flow Diagrams (CFD) and analytics
from Taiga project management data with professional visualizations.

Features:
- Interactive Terminal User Interface (TUI)
- Professional CFD chart generation
- Multiple visualization types (dashboard, trends, distribution)
- CSV export for further analysis
- Authentication management

Version: 2.3.2
Author: Muhammad Zeshan Ayub
Repository: https://github.com/ydrgzm/taiga-cfd-analytics
"""

__version__ = "2.3.2"
__author__ = "Muhammad Zeshan Ayub"
__email__ = "zeshanayub.connect@gmail.com"
__github__ = "https://github.com/ydrgzm"
__license__ = "MIT"
__description__ = "Enterprise-grade CFD analytics system for Taiga with modern TUI"

# Expose main components for advanced users
from .cli import main, ModernTaigaCFDManager

__all__ = ["main", "ModernTaigaCFDManager", "__version__", "__author__"]
