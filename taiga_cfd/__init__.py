#!/usr/bin/env python3
"""
Taiga CFD Analytics - Enterprise Edition
Modern Terminal User Interface for Cumulative Flow Diagram Analytics

A comprehensive interactive tool with beautiful Terminal User Interface
for managing Taiga CFD analytics with rich formatting and colors.

Created by: Muhammad Zeshan Ayub
GitHub: https://github.com/ydrgzm
Email: zeshanayub.connect@gmail.com
Version: 2.2.1

Usage:
    taiga-cfd
    taiga-cfd-analytics  
    taiga-analytics
"""

__version__ = "2.2.1"
__author__ = "Muhammad Zeshan Ayub"
__email__ = "zeshanayub.connect@gmail.com"
__github__ = "https://github.com/ydrgzm"
__license__ = "MIT"
__description__ = "Enterprise-grade CFD analytics system for Taiga with modern TUI"

# Expose main components for advanced users
from .cli import main, ModernTaigaCFDManager

__all__ = ["main", "ModernTaigaCFDManager", "__version__", "__author__"]
