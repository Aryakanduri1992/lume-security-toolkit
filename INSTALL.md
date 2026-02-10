# Installation Guide

## Prerequisites

- Kali Linux (or any Linux distribution with pentesting tools)
- Python 3.8 or higher
- pip3
- sudo/root access (for some commands)

## Quick Install

```bash
# Clone the repository
git clone https://github.com/yourusername/lume-security-toolkit.git
cd lume-security-toolkit

# Install in development mode
sudo pip3 install -e .

# Verify installation
lume --version
```

## Manual Installation

```bash
# Install from source
sudo python3 setup.py install

# Or using pip
sudo pip3 install .
```

## Uninstall

```bash
sudo pip3 uninstall lume-security-toolkit
```

## Verify Pentesting Tools

Lume requires the following tools to be installed:

```bash
# Check if tools are available
which nmap
which gobuster
which nikto
which sqlmap
which hydra
which msfconsole
which whatweb
```

### Installing Missing Tools (Kali Linux)

```bash
sudo apt update
sudo apt install nmap gobuster nikto sqlmap hydra metasploit-framework whatweb -y
```

## First Run

```bash
# Show help
lume --help

# List supported tools
lume --list-tools

# Try a dry-run
lume --dry-run "scan ports on scanme.nmap.org"
```

## Troubleshooting

### Permission Denied
Some commands require root privileges:
```bash
sudo lume "scan ports on 192.168.1.1"
```

### Command Not Found
If `lume` is not found after installation:
```bash
# Add to PATH
export PATH=$PATH:~/.local/bin

# Or reinstall with sudo
sudo pip3 install -e .
```

### Python Version Issues
Ensure Python 3.8+:
```bash
python3 --version
```
