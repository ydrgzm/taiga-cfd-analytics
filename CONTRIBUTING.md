# Contributing to Taiga CFD Analytics

Thank you for your interest in contributing to Taiga CFD Analytics! This document provides guidelines and information for contributors.

## 📋 **Table of Contents**

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Feature Requests](#feature-requests)
- [Development Guidelines](#development-guidelines)

---

## 🤝 **Code of Conduct**

This project adheres to a code of conduct that we expect all participants to uphold:

- **Be respectful**: Treat everyone with respect and kindness
- **Be inclusive**: Welcome people of all backgrounds and skill levels
- **Be constructive**: Focus on what is best for the community
- **Be collaborative**: Work together to improve the project

---

## 🚀 **Getting Started**

### **Prerequisites**
- Python 3.8 or higher
- Git for version control
- Basic knowledge of Python development
- Familiarity with Taiga project management (helpful but not required)

### **Development Setup**

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/taiga-cfd-analytics.git
   cd taiga-cfd-analytics
   ```

2. **Set up development environment**
   ```bash
   # Create virtual environment
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   pip install -e .[dev]
   ```

3. **Set up pre-commit hooks** (optional but recommended)
   ```bash
   pre-commit install
   ```

---

## 🛠️ **How to Contribute**

### **Types of Contributions**

- **🐛 Bug fixes**: Fix issues and improve stability
- **✨ New features**: Add new functionality
- **📚 Documentation**: Improve or add documentation
- **🎨 UI/UX**: Enhance the user interface
- **⚡ Performance**: Optimize performance and efficiency
- **🧪 Testing**: Add or improve tests

### **Areas for Contribution**

- **Core Analytics**: Improve CFD generation algorithms
- **Visualization**: Enhance chart types and styling
- **TUI Interface**: Improve the terminal user interface
- **API Integration**: Enhance Taiga API integration
- **Documentation**: Improve user guides and code documentation
- **Testing**: Add unit tests and integration tests
- **Performance**: Optimize data processing and visualization

---

## 📝 **Pull Request Process**

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the [Development Guidelines](#development-guidelines)
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run tests
   pytest

   # Test the TUI interface
   python3 taiga_cfd_tui.py

   # Check code formatting
   black --check .
   flake8
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new visualization type"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub.

### **PR Requirements**
- Clear description of changes
- Tests for new functionality
- Updated documentation
- No breaking changes (unless discussed)
- Code follows project style guidelines

---

## 🐛 **Issue Reporting**

### **Before Reporting**
- Check existing issues for duplicates
- Try the latest version
- Test in a clean environment

### **Good Bug Reports Include**
- **Environment**: OS, Python version, package versions
- **Steps to reproduce**: Clear, minimal reproduction steps
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Screenshots**: If UI-related
- **Logs**: Any error messages or stack traces

### **Issue Template**
```markdown
**Environment:**
- OS: [e.g., macOS 12.0]
- Python: [e.g., 3.9.7]
- Version: [e.g., 2.1.0]

**Description:**
Brief description of the issue

**Steps to Reproduce:**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Additional Context:**
Any other context, screenshots, or logs
```

---

## 💡 **Feature Requests**

We welcome feature requests! Please:

1. **Check existing requests** to avoid duplicates
2. **Describe the use case** clearly
3. **Explain the benefit** to users
4. **Provide examples** if possible
5. **Consider implementation** complexity

### **Feature Request Template**
```markdown
**Feature Description:**
Clear description of the requested feature

**Use Case:**
Why is this feature needed?

**Proposed Solution:**
How should this work?

**Alternatives Considered:**
Any alternative approaches?

**Additional Context:**
Mockups, examples, or references
```

---

## 📋 **Development Guidelines**

### **Code Style**
- **Python**: Follow PEP 8 style guidelines
- **Formatting**: Use Black for code formatting
- **Linting**: Use flake8 for linting
- **Type Hints**: Use type hints where appropriate
- **Docstrings**: Document functions and classes

### **Naming Conventions**
- **Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Files**: `snake_case.py`

### **Project Structure**
```
taiga-cfd-analytics/
├── taiga_cfd_tui.py          # Main TUI application
├── taiga_cfd_generator.py    # CFD data generation
├── cfd_visualizer.py         # Chart creation
├── requirements.txt          # Dependencies
├── setup.py                  # Package setup
├── README.md                 # Project documentation
├── CONTRIBUTING.md           # This file
├── LICENSE                   # MIT License
├── tests/                    # Test suite
├── docs/                     # Additional documentation
└── archive/                  # Legacy files
```

### **Testing Guidelines**
- **Unit tests**: Test individual functions
- **Integration tests**: Test component interactions
- **TUI tests**: Test user interface components
- **API tests**: Test Taiga API integration
- **Mock external calls**: Use mocks for API calls in tests

### **Documentation Standards**
- **Code comments**: Explain complex logic
- **Docstrings**: Document public functions and classes
- **README updates**: Keep README.md current
- **Inline help**: Update built-in help system

---

## 🏷️ **Commit Message Format**

Use conventional commit messages:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Add or modify tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(visualization): add PDF export functionality
fix(auth): resolve token refresh issue
docs(readme): update installation instructions
```

---

## 🎯 **Development Focus Areas**

### **High Priority**
- Bug fixes and stability improvements
- Performance optimizations
- User experience enhancements
- Documentation improvements

### **Medium Priority**
- New visualization types
- Additional export formats
- Advanced filtering options
- Multi-project support

### **Future Considerations**
- Web interface
- Real-time data streaming
- Advanced analytics features
- API extensions

---

## 📞 **Contact**

- **Maintainer**: [Muhammad Zeshan Ayub](https://github.com/ydrgzm)
- **Email**: zeshanayub.connect@gmail.com
- **GitHub Issues**: [Project Issues](https://github.com/ydrgzm/taiga-cfd-analytics/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ydrgzm/taiga-cfd-analytics/discussions)

---

## 🙏 **Recognition**

Contributors will be recognized in:
- Project README.md
- Release notes
- GitHub contributors list
- Special thanks in documentation

Thank you for contributing to Taiga CFD Analytics! Your efforts help make this project better for everyone. 🚀
