# 🎯 Taiga CFD Analytics - Enterprise Edition

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![Package Version](https://img.shields.io/badge/version-2.1.0-green.svg)](https://github.com/ydrgzm/taiga-cfd-analytics)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)]()

**Enterprise-grade Cumulative Flow Diagram (CFD) analytics system for Taiga project management with modern Terminal User Interface (TUI)**

A comprehensive interactive tool with beautiful terminal interface for managing Taiga CFD analytics with rich formatting, colors, and professional visualizations.

---

## ✨ Features

### 🎨 Modern Terminal User Interface (TUI)
- **Beautiful Interface**: Rich color schemes, panels, and interactive elements
- **Professional Design**: Enterprise-grade user experience with intuitive navigation
- **Real-time Status**: Live system status monitoring and file tracking
- **Interactive Menus**: Validated input system with helpful prompts

### 📊 Advanced CFD Analytics  
- **Flexible Date Ranges**: Preset periods or custom date selection
- **Multiple Granularities**: Daily, weekly, and monthly analysis options
- **Comprehensive Data Export**: Timestamped CSV files for historical analysis
- **Quick Analysis**: One-click preset analysis for common time periods

### 🎭 Visualization Studio
- **📊 Comprehensive Dashboard**: Multi-panel overview with key metrics
- **📈 Stacked Area Charts**: Classic CFD visualization with flow states
- **🥧 Distribution Charts**: Status breakdown with pie and bar charts  
- **📊 Trend Analysis**: Velocity tracking and pattern identification
- **🖼️ Interactive Gallery**: Browse, manage, and export visualizations

### 🔐 Enterprise Security
- **Secure Authentication**: Safe token storage and automatic reuse
- **API Integration**: Direct connection to Taiga's official API
- **Session Management**: Persistent authentication across sessions
- **Token Validation**: Real-time authentication status checking

### 🛠️ System Management
- **Health Diagnostics**: Complete system status and dependency checks
- **Built-in Help**: Comprehensive documentation and usage guides  
- **Error Handling**: Beautiful error messages with helpful suggestions
- **Cross-platform**: Support for macOS, Linux, and Windows

---

## 🚀 Quick Installation

### Install via pip (Recommended)
```bash
# Install the package
pip install taiga-cfd-analytics

# Launch the application
taiga-cfd
```

**That's it!** The system will automatically:
- ✅ Install all required dependencies
- ✅ Set up the beautiful TUI interface
- ✅ Create executable commands (`taiga-cfd`, `taiga-cfd-analytics`, `taiga-analytics`)
- ✅ Handle all system configuration

### Alternative Commands
```bash
# All of these launch the same application:
taiga-cfd                # Short command
taiga-cfd-analytics      # Full name  
taiga-analytics          # Alternative
```

---

## 📖 Usage Guide

### 1. **First Launch**
```bash
taiga-cfd
```
The beautiful TUI will launch with a welcome screen and system status.

### 2. **Authentication Setup** 
- Select **Option 1** from the main menu
- Enter your Taiga credentials (username/email and password)
- Tokens are securely saved for future sessions
- One-time setup with automatic reuse

### 3. **Generate CFD Data**
- Select **Option 2** for interactive CFD generation
- Choose date ranges: preset periods or custom dates
- Select granularity: daily, weekly, or monthly
- System generates CSV data and creates visualizations

### 4. **Quick Analysis** 
- Select **Option 4** for instant 1-month daily analysis
- Perfect for sprint reviews and recent trend analysis
- Automatic data generation and chart creation

### 5. **Visualization Studio**
- Select **Option 3** to access the visualization studio
- Generate charts from latest data or specific CSV files
- Browse the interactive gallery of created visualizations
- Export charts in multiple formats

---

## 🎨 Screenshot Gallery

### Main Menu Interface
```
🎯 TAIGA CFD ANALYTICS
Enterprise Terminal Interface

┌─ System Status ─────────────────────────────────────────┐
│ 🔐 Authentication: ✅ Muhammad Zeshan    📊 CSV Files: 5 files    │
│ 🎯 Project: azeb-admin-empathy         🎨 Visualizations: 12 charts │
└─────────────────────────────────────────────────────────┘

┌─ 🎮 Main Menu ──────────────────────────────────────────┐
│ Option │ Feature                    │ Description           │
├────────┼───────────────────────────┼──────────────────────┤
│   1    │ 🔐 Authentication Setup   │ Configure credentials │
│   2    │ 📈 Generate CFD Data      │ Interactive analysis  │
│   3    │ 🎨 Visualization Studio   │ Create beautiful charts │
│   4    │ ⚡ Quick Analysis         │ Instant 1-month analysis │
│   5    │ 🛠️ System Diagnostics    │ Health monitoring     │
│   6    │ 📚 Help Center           │ Built-in documentation │
│   7    │ 🚪 Exit                  │ Clean shutdown        │
└────────┴───────────────────────────┴──────────────────────┘
```

### Beautiful Progress Indicators
```
🚀 Launching CFD generator...
⠋ Creating professional charts... ████████████████████ 100%
✅ Generation Complete - CFD data and visualizations created successfully!
```

---

## 🔧 System Requirements

### Python Version
- **Python 3.8+** (tested on 3.8, 3.9, 3.10, 3.11, 3.12)

### Operating Systems
- **macOS**: Full support with native integrations
- **Linux**: Complete compatibility across distributions  
- **Windows**: Cross-platform terminal support

### Dependencies
All dependencies are automatically installed with pip:
```
requests>=2.25.1      # API communication
matplotlib>=3.5.0     # Chart generation  
seaborn>=0.11.0       # Statistical visualizations
pandas>=1.3.0         # Data processing
numpy>=1.21.0         # Numerical computations
rich>=13.0.0          # Modern TUI interface
textual>=0.44.0       # Advanced terminal widgets
```

---

## 🎯 Use Cases

### 📊 **Sprint Analysis**
- **Daily granularity** for detailed workflow analysis
- **1-month periods** for sprint retrospectives
- **Quick analysis** option for rapid insights

### 📈 **Quarterly Reviews** 
- **3-month periods** with weekly granularity
- **Trend analysis** for pattern identification
- **Professional charts** for stakeholder presentations

### 🎨 **Executive Reporting**
- **Annual analysis** with monthly granularity
- **Dashboard visualizations** for high-level overview
- **Export capabilities** for board presentations

### 🔍 **Continuous Monitoring**
- **System diagnostics** for health checks
- **Authentication management** for team access
- **Interactive gallery** for historical analysis

---

## 🏗️ Development & Contributing

### Local Development
```bash
# Clone the repository
git clone https://github.com/ydrgzm/taiga-cfd-analytics.git
cd taiga-cfd-analytics

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"

# Run the application
taiga-cfd
```

### Testing
```bash
# Run tests
pytest

# Code formatting
black taiga_cfd/

# Linting
flake8 taiga_cfd/

# Type checking
mypy taiga_cfd/
```

---

## 📚 Documentation

### Built-in Help System
The application includes a comprehensive **Help Center** (Option 6) with:
- **Authentication guides** for secure setup
- **CFD generation tutorials** with best practices
- **Visualization studio** documentation  
- **Granularity selection** guidelines
- **Enterprise tips** for advanced usage

### API Reference
For advanced users, the package exposes:
```python
from taiga_cfd import ModernTaigaCFDManager, main

# Programmatic usage
manager = ModernTaigaCFDManager()
manager.run_interactive_system()
```

---

## 🎖️ Credits & License

### 👨‍💻 **Created by**
**Muhammad Zeshan Ayub**
- 🔗 **GitHub**: [https://github.com/ydrgzm](https://github.com/ydrgzm)
- 📧 **Email**: [zeshanayub.connect@gmail.com](mailto:zeshanayub.connect@gmail.com)
- 🌟 **Version**: 2.1.0 (Enterprise Edition)

### 📄 **License**
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### 🙏 **Acknowledgments**
- **Taiga Team** for the excellent project management platform
- **Rich Library** for beautiful terminal interfaces  
- **Python Community** for amazing data science tools

---

## 🔗 Links

- **📦 PyPI Package**: [https://pypi.org/project/taiga-cfd-analytics/](https://pypi.org/project/taiga-cfd-analytics/)
- **📂 Source Code**: [https://github.com/ydrgzm/taiga-cfd-analytics](https://github.com/ydrgzm/taiga-cfd-analytics)  
- **🐛 Bug Reports**: [https://github.com/ydrgzm/taiga-cfd-analytics/issues](https://github.com/ydrgzm/taiga-cfd-analytics/issues)
- **💬 Discussions**: [https://github.com/ydrgzm/taiga-cfd-analytics/discussions](https://github.com/ydrgzm/taiga-cfd-analytics/discussions)

---

<div align="center">

**⭐ If you find this project useful, please star it on GitHub! ⭐**

[🚀 Install Now](https://pypi.org/project/taiga-cfd-analytics/) | [📖 Documentation](https://github.com/ydrgzm/taiga-cfd-analytics) | [🐛 Report Issues](https://github.com/ydrgzm/taiga-cfd-analytics/issues)

</div>
