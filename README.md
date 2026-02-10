# 🔦 Lume Security Toolkit

**Think in English. Hack in Kali.**

Lume is a command-line tool for Kali Linux that converts plain English instructions into valid penetration testing commands. Perfect for learning, rapid testing, and streamlining your pentesting workflow.

**Version 0.3.0** - Now with **SAFE ML-enhanced natural language understanding**! 🤖

## 🎉 What's New in v0.3.0

- 🤖 **ML Natural Language Normalization** - Understand varied phrasing with spaCy
- 🎯 **Flexible Input** - "first give ip 192.168.1.1 then scan" → works!
- 🔒 **Security-First ML** - ML NEVER generates commands (preprocessor only)
- 📊 **Intent Validation** - Rule engine validates all ML output
- 🔌 **Optional Feature** - Works perfectly without ML (--ml-normalize flag)

[See Full Changelog](CHANGELOG.md) | [ML Feature Guide](ML_FEATURE.md) | [ML Installation](ML_INSTALLATION.md)

---

## ✨ Features

- 🗣️ **Natural Language Interface** - Describe what you want to do in plain English
- 🤖 **ML-Enhanced Understanding** - Handles varied phrasing and word order (optional, NEW!)
- 🛡️ **Safety First** - Always asks for confirmation before executing commands
- 🎯 **Smart Target Detection** - Automatically extracts IPs, domains, and URLs
- 🔧 **Industry-Standard Tools** - Supports nmap, gobuster, nikto, sqlmap, hydra, and more
- 📚 **Educational** - Shows the actual command being executed so you learn
- 🚀 **Zero Dependencies** - Works offline, no API keys or cloud services
- ✅ **Production-Ready** - Audit trails, summaries, and compliance-ready
- 🔒 **Security Guarantees** - ML never generates commands (rule engine is authoritative)

## 🚀 Installation

### Quick Install (Basic - No ML)

```bash
# Clone the repository
git clone https://github.com/Aryakanduri1992/lume-security-toolkit.git
cd lume-security-toolkit

# Install
sudo pip3 install -e . --break-system-packages

# Verify installation
lume --version
```

### ML-Enhanced Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/Aryakanduri1992/lume-security-toolkit.git
cd lume-security-toolkit

# Install with ML support
sudo pip3 install -e ".[ml]" --break-system-packages

# Download spaCy model (12MB)
python -m spacy download en_core_web_sm

# Verify installation
lume --version
lume --ml-normalize "scan 192.168.1.1"
```

**See [ML_INSTALLATION.md](ML_INSTALLATION.md) for detailed installation guide.**

### Requirements

- Python 3.8+
- Kali Linux (or any Linux with pentesting tools installed)
- Root/sudo access for certain commands
- Optional: spaCy for ML features (12MB model)

## 📖 Usage

### Basic Syntax

```bash
lume "your instruction in plain English"
```

### Examples

**Port Scanning**
```bash
lume "scan ports on 192.168.1.1"
lume "find open ports on example.com"
lume "quick scan 10.0.0.5"
```

**Directory Enumeration**
```bash
lume "find admin login page on example.com"
lume "enumerate directories on https://target.com"
lume "discover hidden paths on 192.168.1.100"
```

**Web Vulnerability Scanning**
```bash
lume "scan web vulnerabilities on example.com"
lume "check web security on https://target.com"
```

**SQL Injection Testing**
```bash
lume "test sql injection on http://target.com/page?id=1"
lume "check sql vulnerability on example.com"
```

**Subdomain Enumeration**
```bash
lume "find subdomains of example.com"
lume "enumerate subdomains on target.com"
```

**Brute Force Attacks**
```bash
lume "brute force ssh on 192.168.1.10"
lume "crack ftp password on 10.0.0.5"
```

**Network Discovery**
```bash
lume "scan network for live hosts on 192.168.1.0"
lume "find active hosts on 10.0.0.0"
```

### Options

```bash
# Normal execution (with post-execution summary)
lume "scan ports on 192.168.1.1"

# ML-enhanced normalization (NEW!)
lume --ml-normalize "first give ip 192.168.1.1 then scan"

# Adjust ML confidence threshold (NEW!)
lume --ml-normalize --ml-confidence 0.80 "check example.com"

# Explain mode - understand without executing
lume --explain "scan ports on 192.168.1.1"

# Dry-run mode (show command without executing)
lume --dry-run "scan ports on 192.168.1.1"

# Show execution history
lume --history

# List supported tools
lume --list-tools

# Show version
lume --version

# Show help
lume --help
```

### ML Feature Examples (v0.3.0)

**Flexible Phrasing:**
```bash
$ lume --ml-normalize "first give ip 192.168.1.1 then scan"

🤖 ML normalization enabled
✓ ML normalized input (confidence: 0.85)
Original: first give ip 192.168.1.1 then scan
Normalized: scan ports on 192.168.1.1

[Tool] nmap
[Command] nmap -sV -T4 192.168.1.1
...
```

**Synonym Handling:**
```bash
$ lume --ml-normalize "enumerate admin pages on example.com"

🤖 ML normalization enabled
✓ ML normalized input (confidence: 0.80)
Original: enumerate admin pages on example.com
Normalized: find directories on example.com

[Tool] gobuster
...
```

**See [ML_FEATURE.md](ML_FEATURE.md) for complete ML documentation.**

### Example Output (v0.2.0)

**Normal Execution:**
```bash
$ lume "scan ports on 192.168.70.1"

[Command executes...]

✔ Action Summary:
  • Performed a service and version scan on the target
  • Identified open ports and detected running network services for further analysis
```

**Explain Mode:**
```bash
$ lume --explain "find admin page on example.com"

[Explanation Mode]

Tool: gobuster
Command: gobuster dir -u example.com -w /usr/share/wordlists/...

What it does:
  • Performed directory and file enumeration on web server
  • Discovered hidden paths, admin panels, and accessible web resources

⚠️  Directory brute-forcing generates significant traffic. Use responsibly.
```

## 🎯 Supported Tools

- **nmap** - Network scanning and port discovery
- **gobuster** - Directory/file and DNS enumeration
- **nikto** - Web server vulnerability scanning
- **sqlmap** - SQL injection testing
- **hydra** - Password brute-forcing
- **metasploit** - Exploitation framework (basic commands)
- **whatweb** - Web technology identification

## 🔒 Security & Ethics

### ⚠️ Important Warnings

- **Authorization Required**: Only use Lume on systems you own or have explicit permission to test
- **Educational Purpose**: This tool is for learning and authorized security testing only
- **Legal Responsibility**: Unauthorized access to computer systems is illegal
- **Confirmation Required**: Lume always asks before executing commands
- **Audit Trail**: All commands are visible before execution

### Ethical Use Guidelines

1. ✅ Use on your own systems or lab environments
2. ✅ Use with written authorization from system owners
3. ✅ Use for security research and education
4. ❌ Never use on systems without permission
5. ❌ Never use for malicious purposes
6. ❌ Never use to cause harm or disruption

## 🏗️ Project Structure

```
lume-security-toolkit/
├── lume/
│   ├── __init__.py
│   ├── cli.py              # Main CLI entry point
│   ├── core/
│   │   ├── __init__.py
│   │   └── engine.py       # Command parsing and execution
│   ├── ml/                 # NEW: ML normalization module
│   │   ├── __init__.py
│   │   └── normalizer.py   # spaCy-based normalizer
│   ├── utils/
│   │   ├── __init__.py
│   │   └── display.py      # CLI output formatting
│   └── data/
│       └── rules.json      # Command mapping rules
├── setup.py
├── README.md
├── ML_FEATURE.md           # NEW: ML documentation
├── ML_INSTALLATION.md      # NEW: ML installation guide
└── LICENSE
```

## 🛠️ How It Works

### Basic Flow (Rule-Based)
1. **Input Parsing**: Lume analyzes your English instruction
2. **Pattern Matching**: Matches against rule-based patterns
3. **Target Extraction**: Identifies IPs, domains, or URLs
4. **Command Generation**: Builds the appropriate pentesting command
5. **User Confirmation**: Shows the command and asks for approval
6. **Execution**: Runs the command if confirmed

### ML-Enhanced Flow (Optional)
1. **Input Parsing**: User provides natural language instruction
2. **ML Normalization**: spaCy extracts intent and target
3. **Canonical Instruction**: ML produces standardized English
4. **Validation**: Rule engine validates ML output
5. **Pattern Matching**: Matches canonical instruction to rules
6. **Command Generation**: Builds the pentesting command
7. **User Confirmation**: Shows command and asks for approval
8. **Execution**: Runs the command if confirmed

**Key Principle**: ML only normalizes language. The rule engine generates ALL commands.

See [ML_FEATURE.md](ML_FEATURE.md) for detailed ML architecture.

## 🔮 Roadmap

### v0.3.0 ✅ COMPLETE
- [x] ML natural language normalization
- [x] spaCy integration (offline, safe)
- [x] Intent validation layer
- [x] ML audit logging
- [x] Comprehensive ML documentation

### v0.4.0 (Planned)
- [ ] Report generation (PDF/HTML)
- [ ] Success/failure detection
- [ ] Next-step recommendations
- [ ] Custom wordlist support
- [ ] Output parsing and formatting
- [ ] More tool integrations (wpscan, enum4linux, etc.)

### v1.0.0 (Vision)
- [ ] Custom intent training
- [ ] Interactive mode
- [ ] Workflow automation
- [ ] Team collaboration features
- [ ] Plugin system for custom tools

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚖️ Disclaimer

This tool is provided for educational and ethical security testing purposes only. The developers assume no liability and are not responsible for any misuse or damage caused by this program. Users are responsible for complying with all applicable laws and regulations.

## 🙏 Acknowledgments

- Inspired by the Kali Linux community
- Built for ethical hackers and security professionals
- Thanks to all pentesting tool developers

## 📧 Contact

- GitHub: [@Aryakanduri1992](https://github.com/Aryakanduri1992)
- Repository: [lume-security-toolkit](https://github.com/Aryakanduri1992/lume-security-toolkit)
- Issues: [GitHub Issues](https://github.com/Aryakanduri1992/lume-security-toolkit/issues)

---

**Remember: With great power comes great responsibility. Hack ethically. 🔒**
