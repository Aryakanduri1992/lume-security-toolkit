# Contributing to Lume Security Toolkit

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and professional
- Focus on ethical security practices
- Help maintain a welcoming environment
- Report security issues responsibly

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Use the GitHub issue tracker
3. Include:
   - Lume version (`lume --version`)
   - Operating system
   - Python version
   - Steps to reproduce
   - Expected vs actual behavior

### Suggesting Features

1. Open a GitHub issue with the "enhancement" label
2. Describe the feature and use case
3. Explain why it would be useful
4. Consider implementation approach

### Adding New Tool Support

To add support for a new pentesting tool:

1. Add patterns and commands to `lume/data/rules.json`
2. Update the engine if special parsing is needed
3. Test thoroughly
4. Update documentation

Example rule:
```json
{
  "tool": "wpscan",
  "patterns": [
    "scan.*wordpress",
    "wpscan"
  ],
  "command": "wpscan --url {target} --enumerate",
  "description": "Scan WordPress site for vulnerabilities",
  "warning": "WordPress scanning may be detected by security plugins."
}
```

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small
- Comment complex logic

### Testing

Before submitting:
```bash
# Test installation
pip3 install -e .

# Test basic functionality
lume --version
lume --list-tools
lume --dry-run "scan ports on 127.0.0.1"

# Test with actual commands (on authorized targets only)
lume "scan ports on scanme.nmap.org"
```

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

### Commit Messages

Use clear, descriptive commit messages:
```
Add support for wpscan tool

- Added wpscan patterns to rules.json
- Updated documentation
- Tested on WordPress test site
```

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/lume-security-toolkit.git
cd lume-security-toolkit

# Create virtual environment (optional)
python3 -m venv venv
source venv/bin/activate

# Install in development mode
pip3 install -e .

# Make changes and test
lume --dry-run "your test command"
```

## Project Structure

```
lume/
├── cli.py          # CLI entry point
├── core/
│   └── engine.py   # Command parsing logic
├── utils/
│   └── display.py  # Output formatting
└── data/
    └── rules.json  # Command mappings
```

## Questions?

Open an issue or reach out to the maintainers.

Thank you for contributing to Lume! 🔦
