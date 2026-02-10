# 🔦 Lume Security Toolkit

**Think in English. Hack in Kali.**

Lume is a command-line tool for Kali Linux that converts plain English instructions into valid penetration testing commands. Perfect for learning, rapid testing, and streamlining your pentesting workflow.

## ✨ Features

- 🗣️ **Natural Language Interface** - Describe what you want to do in plain English
- 🛡️ **Safety First** - Always asks for confirmation before executing commands
- 🎯 **Smart Target Detection** - Automatically extracts IPs, domains, and URLs
- 🔧 **Industry-Standard Tools** - Supports nmap, gobuster, nikto, sqlmap, hydra, and more
- 📚 **Educational** - Shows the actual command being executed so you learn
- 🚀 **No Dependencies** - Pure Python, no API keys or LLM required

## 🚀 Installation

### From GitHub

```bash
# Clone the repository
git clone https://github.com/yourusername/lume-security-toolkit.git
cd lume-security-toolkit

# Install
sudo pip3 install -e .

# Verify installation
lume --version
```

### Requirements

- Python 3.8+
- Kali Linux (or any Linux with pentesting tools installed)
- Root/sudo access for certain commands

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
# Dry-run mode (show command without executing)
lume --dry-run "scan ports on 192.168.1.1"

# List supported tools
lume --list-tools

# Show version
lume --version

# Show help
lume --help
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
│   ├── utils/
│   │   ├── __init__.py
│   │   └── display.py      # CLI output formatting
│   └── data/
│       └── rules.json      # Command mapping rules
├── setup.py
├── README.md
└── LICENSE
```

## 🛠️ How It Works

1. **Input Parsing**: Lume analyzes your English instruction
2. **Pattern Matching**: Matches against rule-based patterns
3. **Target Extraction**: Identifies IPs, domains, or URLs
4. **Command Generation**: Builds the appropriate pentesting command
5. **User Confirmation**: Shows the command and asks for approval
6. **Execution**: Runs the command if confirmed

## 🔮 Roadmap

### v0.2.0 (Planned)
- [ ] Command history and logging
- [ ] Custom wordlist support
- [ ] Output parsing and formatting
- [ ] More tool integrations (wpscan, enum4linux, etc.)

### v0.3.0 (Future)
- [ ] Plugin system for custom tools
- [ ] Learning mode with explanations
- [ ] Command chaining support
- [ ] Report generation

### v1.0.0 (Vision)
- [ ] Optional AI/LLM integration
- [ ] Interactive mode
- [ ] Workflow automation
- [ ] Team collaboration features

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

- GitHub: [@yourusername](https://github.com/yourusername)
- Issues: [GitHub Issues](https://github.com/yourusername/lume-security-toolkit/issues)

---

**Remember: With great power comes great responsibility. Hack ethically. 🔒**
