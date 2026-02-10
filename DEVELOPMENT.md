# Development Guide

## Getting Started

### Prerequisites
- Python 3.8+
- Git
- Kali Linux or Linux with pentesting tools
- Text editor or IDE

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/lume-security-toolkit.git
cd lume-security-toolkit

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip3 install -e .

# Verify installation
lume --version
```

## Project Structure

```
lume/
├── __init__.py          # Package metadata
├── cli.py              # Main CLI entry point
├── core/
│   ├── __init__.py
│   └── engine.py       # Core parsing and execution logic
├── utils/
│   ├── __init__.py
│   └── display.py      # CLI output formatting
└── data/
    └── rules.json      # Command mapping rules
```

## Adding a New Tool

### Step 1: Add Rule to rules.json

```json
{
  "tool": "wpscan",
  "patterns": [
    "scan.*wordpress",
    "wordpress.*scan",
    "wpscan"
  ],
  "command": "wpscan --url {target} --enumerate",
  "description": "Scan WordPress site for vulnerabilities",
  "warning": "WordPress scanning may be detected by security plugins."
}
```

### Step 2: Add Special Handling (if needed)

Edit `lume/core/engine.py` in the `_build_command()` method:

```python
elif rule['tool'] == 'wpscan':
    # Extract specific options from instruction
    if 'plugin' in instruction:
        command = command.replace('--enumerate', '--enumerate p')
    elif 'theme' in instruction:
        command = command.replace('--enumerate', '--enumerate t')
```

### Step 3: Test

```bash
# Test in dry-run mode
lume --dry-run "scan wordpress on example.com"

# Test actual execution (on authorized target)
lume "scan wordpress on testsite.local"
```

### Step 4: Document

Add examples to `EXAMPLES.md`:

```markdown
**WordPress Scanning**
```bash
lume "scan wordpress on example.com"
```

## Code Style

### Python Style Guide

Follow PEP 8:
```python
# Good
def parse_instruction(self, instruction: str) -> Optional[Dict]:
    """Parse natural language instruction into a command"""
    pass

# Bad
def parseInstruction(self,instruction):
    pass
```

### Naming Conventions

- **Classes:** PascalCase (`LumeEngine`)
- **Functions:** snake_case (`parse_instruction`)
- **Constants:** UPPER_SNAKE_CASE (`DEFAULT_TIMEOUT`)
- **Private methods:** _leading_underscore (`_extract_target`)

### Documentation

Use docstrings:
```python
def parse_instruction(self, instruction: str) -> Optional[Dict]:
    """
    Parse natural language instruction into a command
    
    Args:
        instruction: Natural language string from user
        
    Returns:
        Dictionary with tool, command, description, and warning
        Returns None if instruction cannot be parsed
    """
    pass
```

## Testing

### Manual Testing

```bash
# Run test suite
./test_lume.sh

# Run demo
./demo.sh
```

### Test Checklist

- [ ] Installation works
- [ ] `--version` flag works
- [ ] `--help` flag works
- [ ] `--list-tools` flag works
- [ ] Dry-run mode works
- [ ] Target extraction works (IP, domain, URL)
- [ ] Pattern matching works
- [ ] Command generation works
- [ ] Confirmation prompt works
- [ ] Command execution works (on authorized target)

### Adding Unit Tests (Future)

```python
# tests/test_engine.py
import unittest
from lume.core.engine import LumeEngine

class TestEngine(unittest.TestCase):
    def setUp(self):
        self.engine = LumeEngine()
    
    def test_extract_ip(self):
        instruction = "scan ports on 192.168.1.1"
        target = self.engine._extract_target(instruction)
        self.assertEqual(target, "192.168.1.1")
    
    def test_parse_port_scan(self):
        instruction = "scan ports on 192.168.1.1"
        result = self.engine.parse_instruction(instruction)
        self.assertEqual(result['tool'], 'nmap')
        self.assertIn('192.168.1.1', result['command'])
```

## Debugging

### Enable Debug Mode

Add to `cli.py`:
```python
import logging

# Add after imports
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Use in code
logger.debug(f"Parsed instruction: {instruction}")
logger.debug(f"Matched rule: {rule}")
```

### Common Issues

**Issue:** Command not found after installation
```bash
# Solution: Add to PATH
export PATH=$PATH:~/.local/bin

# Or reinstall with sudo
sudo pip3 install -e .
```

**Issue:** Rules not loading
```bash
# Check rules.json syntax
python3 -m json.tool lume/data/rules.json

# Verify file is included
python3 -c "from lume.core.engine import LumeEngine; e = LumeEngine(); print(e.rules)"
```

**Issue:** Pattern not matching
```python
# Test regex pattern
import re
pattern = r"scan.*port"
instruction = "scan ports on 192.168.1.1"
print(re.search(pattern, instruction, re.IGNORECASE))
```

## Performance Optimization

### Profiling

```python
import cProfile
import pstats

# Profile the engine
profiler = cProfile.Profile()
profiler.enable()

engine = LumeEngine()
result = engine.parse_instruction("scan ports on 192.168.1.1")

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

### Optimization Tips

1. **Compile regex patterns once**
```python
# In __init__
self.compiled_patterns = {
    rule['tool']: [re.compile(p, re.IGNORECASE) for p in rule['patterns']]
    for rule in self.rules['rules']
}
```

2. **Cache rules loading**
3. **Use efficient data structures**
4. **Minimize subprocess overhead**

## Release Process

### Version Bumping

1. Update version in `lume/__init__.py`
2. Update version in `setup.py`
3. Update CHANGELOG.md
4. Commit changes
5. Tag release

```bash
git add .
git commit -m "Bump version to 0.2.0"
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin main --tags
```

### Creating a Release

1. Create GitHub release
2. Upload distribution files
3. Update documentation
4. Announce on social media

## Contributing Workflow

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Open Pull Request

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

Example:
```
feat: Add wpscan support

- Added wpscan patterns to rules.json
- Implemented plugin/theme enumeration options
- Updated documentation with examples

Closes #42
```

## Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Getting Help

- Open an issue on GitHub
- Check existing issues and PRs
- Read the documentation
- Ask in discussions

Happy coding! 🚀
