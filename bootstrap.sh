#!/bin/bash
# Lume Security Toolkit - Bootstrap Installer
# One-command installer that creates the entire project from scratch
# Usage: curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/lume-security-toolkit/main/bootstrap.sh | bash

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
NC='\033[0m'

clear
echo -e "${CYAN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                        🔦 LUME SECURITY TOOLKIT 🔦                           ║
║                                                                              ║
║                     Think in English. Hack in Kali.                          ║
║                                                                              ║
║                        Bootstrap Installer v1.0                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}\n"

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${YELLOW}⚠️  Warning: Running as root. This is not recommended.${NC}"
    read -p "Continue anyway? [y/N]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Step 1: Check prerequisites
echo -e "${BLUE}[1/8] Checking prerequisites...${NC}"

# Check Python
if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo -e "${GREEN}✓ Python $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python 3.8+ required${NC}"
    echo "Install: sudo apt install python3 python3-pip -y"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓ pip3 found${NC}"
else
    echo -e "${YELLOW}⚠️  pip3 not found, installing...${NC}"
    sudo apt update && sudo apt install python3-pip -y
fi

# Check git
if command -v git &> /dev/null; then
    echo -e "${GREEN}✓ git found${NC}"
else
    echo -e "${YELLOW}⚠️  git not found, installing...${NC}"
    sudo apt install git -y
fi

# Step 2: Create project directory
echo -e "\n${BLUE}[2/8] Creating project structure...${NC}"

PROJECT_DIR="$HOME/lume-security-toolkit"

if [ -d "$PROJECT_DIR" ]; then
    echo -e "${YELLOW}⚠️  Directory $PROJECT_DIR already exists${NC}"
    read -p "Remove and reinstall? [y/N]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$PROJECT_DIR"
    else
        echo "Installation cancelled"
        exit 1
    fi
fi

mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Create directory structure
mkdir -p lume/{core,utils,data}

echo -e "${GREEN}✓ Directory structure created${NC}"

# Step 3: Create Python files
echo -e "\n${BLUE}[3/8] Creating Python modules...${NC}"

# lume/__init__.py
cat > lume/__init__.py << 'PYEOF'
"""
Lume Security Toolkit
Think in English. Hack in Kali.
"""

__version__ = "0.1.0"
__author__ = "Lume Security Team"
PYEOF

# lume/core/__init__.py
echo '"""Core engine module"""' > lume/core/__init__.py

# lume/utils/__init__.py
echo '"""Utility modules"""' > lume/utils/__init__.py

# lume/cli.py
cat > lume/cli.py << 'PYEOF'
#!/usr/bin/env python3
"""
Lume CLI - Main entry point
"""

import sys
import argparse
from lume.core.engine import LumeEngine
from lume.utils.display import Display
from lume import __version__


def main():
    parser = argparse.ArgumentParser(
        prog='lume',
        description='Lume Security Toolkit - Think in English. Hack in Kali.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  lume "scan network for live hosts"
  lume "find admin login page on example.com"
  lume "brute force ssh on 192.168.1.10"
  lume --dry-run "enumerate subdomains"
  
For more information: https://github.com/yourusername/lume-security-toolkit
        """
    )
    
    parser.add_argument(
        'instruction',
        nargs='?',
        help='Natural language pentesting instruction'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show command without executing'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'Lume Security Toolkit v{__version__}'
    )
    
    parser.add_argument(
        '--list-tools',
        action='store_true',
        help='List all supported pentesting tools'
    )
    
    args = parser.parse_args()
    
    display = Display()
    engine = LumeEngine()
    
    # Show banner
    display.banner()
    
    # List tools if requested
    if args.list_tools:
        display.list_tools(engine.get_supported_tools())
        sys.exit(0)
    
    # Require instruction
    if not args.instruction:
        parser.print_help()
        sys.exit(1)
    
    try:
        # Parse instruction
        result = engine.parse_instruction(args.instruction)
        
        if not result:
            display.error("Could not understand the instruction. Try being more specific.")
            display.info("Example: lume \"scan ports on 192.168.1.1\"")
            sys.exit(1)
        
        # Display the generated command
        display.show_command(result)
        
        # Dry run mode
        if args.dry_run:
            display.info("Dry-run mode: Command not executed")
            sys.exit(0)
        
        # Ask for confirmation
        if not display.confirm_execution():
            display.warning("Execution cancelled by user")
            sys.exit(0)
        
        # Execute command
        display.info("Executing command...")
        exit_code = engine.execute_command(result['command'])
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        display.warning("\nOperation cancelled by user")
        sys.exit(130)
    except Exception as e:
        display.error(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
PYEOF

echo -e "${GREEN}✓ CLI module created${NC}"

# lume/core/engine.py
cat > lume/core/engine.py << 'PYEOF'
"""
Lume Engine - Core command parsing and execution logic
"""

import re
import json
import subprocess
from pathlib import Path
from typing import Dict, Optional, List


class LumeEngine:
    def __init__(self):
        self.rules = self._load_rules()
    
    def _load_rules(self) -> Dict:
        """Load command mapping rules from JSON file"""
        rules_path = Path(__file__).parent.parent / 'data' / 'rules.json'
        with open(rules_path, 'r') as f:
            return json.load(f)
    
    def parse_instruction(self, instruction: str) -> Optional[Dict]:
        """
        Parse natural language instruction into a command
        Returns: {
            'tool': str,
            'command': str,
            'description': str,
            'warning': str
        }
        """
        instruction = instruction.lower().strip()
        
        # Extract target (IP, domain, URL)
        target = self._extract_target(instruction)
        
        # Match against rules
        for rule in self.rules['rules']:
            for pattern in rule['patterns']:
                if re.search(pattern, instruction, re.IGNORECASE):
                    command = self._build_command(rule, target, instruction)
                    return {
                        'tool': rule['tool'],
                        'command': command,
                        'description': rule['description'],
                        'warning': rule.get('warning', 'This command will interact with the target system.')
                    }
        
        return None
    
    def _extract_target(self, instruction: str) -> Optional[str]:
        """Extract IP address, domain, or URL from instruction"""
        # IP address pattern
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ip_match = re.search(ip_pattern, instruction)
        if ip_match:
            return ip_match.group(0)
        
        # Domain pattern
        domain_pattern = r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b'
        domain_match = re.search(domain_pattern, instruction)
        if domain_match:
            return domain_match.group(0)
        
        # URL pattern
        url_pattern = r'https?://[^\s]+'
        url_match = re.search(url_pattern, instruction)
        if url_match:
            return url_match.group(0)
        
        return None
    
    def _build_command(self, rule: Dict, target: Optional[str], instruction: str) -> str:
        """Build the actual command from rule template"""
        command = rule['command']
        
        # Replace target placeholder
        if target:
            command = command.replace('{target}', target)
        else:
            command = command.replace('{target}', '<TARGET>')
        
        # Handle special cases based on instruction keywords
        if rule['tool'] == 'nmap':
            if 'fast' in instruction or 'quick' in instruction:
                command = command.replace('-sV', '-F')
            elif 'aggressive' in instruction:
                command = command.replace('-sV', '-A')
        
        elif rule['tool'] == 'gobuster':
            if 'common' in instruction:
                command = command.replace('{wordlist}', '/usr/share/wordlists/dirb/common.txt')
            else:
                command = command.replace('{wordlist}', '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt')
        
        elif rule['tool'] == 'hydra':
            if 'ssh' in instruction:
                command = command.replace('{service}', 'ssh')
            elif 'ftp' in instruction:
                command = command.replace('{service}', 'ftp')
            elif 'http' in instruction or 'web' in instruction:
                command = command.replace('{service}', 'http-post-form')
        
        return command
    
    def execute_command(self, command: str) -> int:
        """Execute the command and return exit code"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                text=True
            )
            return result.returncode
        except Exception as e:
            print(f"Execution error: {str(e)}")
            return 1
    
    def get_supported_tools(self) -> List[str]:
        """Return list of supported tools"""
        return list(set(rule['tool'] for rule in self.rules['rules']))
PYEOF

echo -e "${GREEN}✓ Engine module created${NC}"

# lume/utils/display.py
cat > lume/utils/display.py << 'PYEOF'
"""
Display utilities for CLI output
"""

import sys
from typing import Dict, List


class Display:
    # ANSI color codes
    COLORS = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m',
        'bold': '\033[1m'
    }
    
    def banner(self):
        """Display Lume banner"""
        banner = f"""
{self.COLORS['cyan']}{self.COLORS['bold']}
╦  ╦ ╦╔╦╗╔═╗
║  ║ ║║║║║╣ 
╩═╝╚═╝╩ ╩╚═╝
{self.COLORS['reset']}{self.COLORS['cyan']}Security Toolkit v0.1.0
Think in English. Hack in Kali.{self.COLORS['reset']}
"""
        print(banner)
    
    def show_command(self, result: Dict):
        """Display the generated command"""
        print(f"\n{self.COLORS['bold']}[Tool]{self.COLORS['reset']} {result['tool']}")
        print(f"{self.COLORS['bold']}[Description]{self.COLORS['reset']} {result['description']}")
        print(f"\n{self.COLORS['green']}{self.COLORS['bold']}[Command]{self.COLORS['reset']}")
        print(f"  {result['command']}\n")
        
        # Show warning
        print(f"{self.COLORS['yellow']}⚠️  {result['warning']}{self.COLORS['reset']}\n")
    
    def confirm_execution(self) -> bool:
        """Ask user for confirmation"""
        try:
            response = input(f"{self.COLORS['bold']}Execute this command? [y/N]: {self.COLORS['reset']}").strip().lower()
            return response in ['y', 'yes']
        except (EOFError, KeyboardInterrupt):
            return False
    
    def info(self, message: str):
        """Display info message"""
        print(f"{self.COLORS['blue']}ℹ️  {message}{self.COLORS['reset']}")
    
    def warning(self, message: str):
        """Display warning message"""
        print(f"{self.COLORS['yellow']}⚠️  {message}{self.COLORS['reset']}")
    
    def error(self, message: str):
        """Display error message"""
        print(f"{self.COLORS['red']}❌ {message}{self.COLORS['reset']}", file=sys.stderr)
    
    def success(self, message: str):
        """Display success message"""
        print(f"{self.COLORS['green']}✓ {message}{self.COLORS['reset']}")
    
    def list_tools(self, tools: List[str]):
        """Display supported tools"""
        print(f"\n{self.COLORS['bold']}Supported Pentesting Tools:{self.COLORS['reset']}\n")
        for tool in sorted(tools):
            print(f"  • {tool}")
        print()
PYEOF

echo -e "${GREEN}✓ Display module created${NC}"

# Step 4: Create rules.json
echo -e "\n${BLUE}[4/8] Creating rules database...${NC}"

cat > lume/data/rules.json << 'JSONEOF'
{
  "rules": [
    {
      "tool": "nmap",
      "patterns": [
        "scan.*port",
        "port.*scan",
        "find.*open.*port",
        "check.*port",
        "network.*scan",
        "scan.*host",
        "discover.*service"
      ],
      "command": "nmap -sV -T4 {target}",
      "description": "Scan target for open ports and services",
      "warning": "Port scanning may trigger IDS/IPS systems. Ensure you have authorization."
    },
    {
      "tool": "nmap",
      "patterns": [
        "scan.*network",
        "find.*live.*host",
        "discover.*host",
        "ping.*sweep"
      ],
      "command": "nmap -sn {target}/24",
      "description": "Discover live hosts on network",
      "warning": "Network scanning may be detected. Ensure you have authorization."
    },
    {
      "tool": "gobuster",
      "patterns": [
        "find.*director",
        "enumerate.*director",
        "directory.*brute",
        "find.*hidden.*page",
        "discover.*path",
        "find.*admin.*page"
      ],
      "command": "gobuster dir -u {target} -w {wordlist} -t 50",
      "description": "Enumerate directories and files on web server",
      "warning": "Directory brute-forcing generates significant traffic. Use responsibly."
    },
    {
      "tool": "gobuster",
      "patterns": [
        "find.*subdomain",
        "enumerate.*subdomain",
        "subdomain.*brute",
        "discover.*subdomain"
      ],
      "command": "gobuster dns -d {target} -w /usr/share/wordlists/dnsmap.txt -t 50",
      "description": "Enumerate subdomains",
      "warning": "DNS enumeration may be logged. Ensure you have authorization."
    },
    {
      "tool": "nikto",
      "patterns": [
        "scan.*web.*vulnerabilit",
        "web.*server.*scan",
        "check.*web.*security",
        "nikto.*scan"
      ],
      "command": "nikto -h {target}",
      "description": "Scan web server for vulnerabilities",
      "warning": "Nikto scans are noisy and easily detected. Use with caution."
    },
    {
      "tool": "sqlmap",
      "patterns": [
        "sql.*injection",
        "test.*sql.*injection",
        "check.*sql.*vuln",
        "sqlmap"
      ],
      "command": "sqlmap -u {target} --batch --banner",
      "description": "Test for SQL injection vulnerabilities",
      "warning": "SQL injection testing may damage databases. Only test authorized systems."
    },
    {
      "tool": "hydra",
      "patterns": [
        "brute.*force.*ssh",
        "crack.*ssh.*password",
        "brute.*ssh"
      ],
      "command": "hydra -L /usr/share/wordlists/metasploit/unix_users.txt -P /usr/share/wordlists/rockyou.txt {target} {service}",
      "description": "Brute force authentication",
      "warning": "Brute force attacks may lock accounts and are easily detected. Use carefully."
    },
    {
      "tool": "hydra",
      "patterns": [
        "brute.*force.*ftp",
        "crack.*ftp.*password",
        "brute.*ftp"
      ],
      "command": "hydra -L /usr/share/wordlists/metasploit/unix_users.txt -P /usr/share/wordlists/rockyou.txt {target} {service}",
      "description": "Brute force FTP authentication",
      "warning": "Brute force attacks may lock accounts and are easily detected. Use carefully."
    },
    {
      "tool": "metasploit",
      "patterns": [
        "exploit.*eternal.*blue",
        "ms17.*010",
        "smb.*exploit"
      ],
      "command": "msfconsole -q -x 'use exploit/windows/smb/ms17_010_eternalblue; set RHOSTS {target}; check; exit'",
      "description": "Check for EternalBlue vulnerability (MS17-010)",
      "warning": "Exploitation can crash systems. Only use on authorized test systems."
    },
    {
      "tool": "nmap",
      "patterns": [
        "os.*detection",
        "detect.*operating.*system",
        "fingerprint.*os",
        "identify.*os"
      ],
      "command": "nmap -O {target}",
      "description": "Detect operating system",
      "warning": "OS detection requires root privileges and may be detected."
    },
    {
      "tool": "nmap",
      "patterns": [
        "vulnerability.*scan",
        "vuln.*scan",
        "check.*vulnerabilit"
      ],
      "command": "nmap --script vuln {target}",
      "description": "Scan for known vulnerabilities using NSE scripts",
      "warning": "Vulnerability scanning may trigger security alerts."
    },
    {
      "tool": "whatweb",
      "patterns": [
        "identify.*web.*technolog",
        "fingerprint.*web",
        "detect.*cms",
        "what.*web.*server"
      ],
      "command": "whatweb {target}",
      "description": "Identify web technologies and CMS",
      "warning": "Web fingerprinting is generally safe but may be logged."
    }
  ]
}
JSONEOF

echo -e "${GREEN}✓ Rules database created${NC}"

# Step 5: Create setup.py
echo -e "\n${BLUE}[5/8] Creating setup.py...${NC}"

cat > setup.py << 'PYEOF'
#!/usr/bin/env python3
"""
Setup script for Lume Security Toolkit
"""

from setuptools import setup, find_packages
from pathlib import Path

readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="lume-security-toolkit",
    version="0.1.0",
    author="Lume Security Team",
    author_email="security@lume.dev",
    description="Think in English. Hack in Kali. - Natural language pentesting CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/lume-security-toolkit",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'lume': ['data/*.json'],
    },
    entry_points={
        'console_scripts': [
            'lume=lume.cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
    install_requires=[],
    keywords="pentesting security kali-linux cybersecurity ethical-hacking cli",
)
PYEOF

echo -e "${GREEN}✓ setup.py created${NC}"

# Step 6: Create MANIFEST.in
cat > MANIFEST.in << 'EOF'
include README.md
include LICENSE
recursive-include lume/data *.json
EOF

# Step 7: Create README.md
echo -e "\n${BLUE}[6/8] Creating documentation...${NC}"

cat > README.md << 'EOF'
# 🔦 Lume Security Toolkit

**Think in English. Hack in Kali.**

Natural language pentesting CLI for Kali Linux.

## Quick Start

```bash
# Install
sudo pip3 install -e .

# Use
lume "scan ports on scanme.nmap.org"
lume --dry-run "find admin page on example.com"
lume --list-tools
```

## Features

✅ Natural language interface
✅ 7 supported tools (nmap, gobuster, nikto, sqlmap, hydra, metasploit, whatweb)
✅ Safety confirmations
✅ Dry-run mode
✅ No dependencies

## Examples

```bash
lume "scan ports on 192.168.1.1"
lume "find admin page on example.com"
lume "test sql injection on http://target.com/page?id=1"
lume "find subdomains of example.com"
```

## ⚠️ Legal Notice

Only use on authorized systems. Unauthorized access is illegal.

## License

MIT License - See LICENSE file
EOF

echo -e "${GREEN}✓ README created${NC}"

# Step 8: Install Lume
echo -e "\n${BLUE}[7/8] Installing Lume...${NC}"

sudo pip3 install -e . 2>&1 | grep -E "(Successfully|Requirement|Installing)" || true

if command -v lume &> /dev/null; then
    echo -e "${GREEN}✓ Lume installed successfully${NC}"
else
    echo -e "${YELLOW}⚠️  Adding to PATH...${NC}"
    export PATH=$PATH:~/.local/bin
    
    if ! grep -q "export PATH=\$PATH:~/.local/bin" ~/.bashrc; then
        echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
    fi
fi

# Step 9: Verify installation
echo -e "\n${BLUE}[8/8] Verifying installation...${NC}"

if command -v lume &> /dev/null; then
    echo -e "${GREEN}✓ lume command available${NC}"
    lume --version 2>&1 | head -5
else
    echo -e "${RED}✗ lume command not found${NC}"
    echo "Try: export PATH=\$PATH:~/.local/bin"
    echo "Or restart your terminal"
fi

# Check pentesting tools
echo -e "\n${BLUE}Checking pentesting tools...${NC}"
TOOLS=("nmap" "gobuster" "nikto" "sqlmap" "hydra" "msfconsole" "whatweb")
MISSING=()

for tool in "${TOOLS[@]}"; do
    if command -v $tool &> /dev/null; then
        echo -e "${GREEN}✓ $tool${NC}"
    else
        echo -e "${YELLOW}⚠ $tool (not found)${NC}"
        MISSING+=($tool)
    fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
    echo -e "\n${YELLOW}Missing tools: ${MISSING[*]}${NC}"
    echo "Install with: sudo apt install nmap gobuster nikto sqlmap hydra metasploit-framework whatweb -y"
fi

# Success message
echo -e "\n${GREEN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                      ✅ INSTALLATION COMPLETE! ✅                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${CYAN}Quick Start Commands:${NC}"
echo "  lume --version"
echo "  lume --list-tools"
echo "  lume --dry-run \"scan ports on 192.168.1.1\""
echo "  lume \"scan ports on scanme.nmap.org\""
echo ""
echo -e "${CYAN}Project Location:${NC}"
echo "  $PROJECT_DIR"
echo ""
echo -e "${YELLOW}⚠️  Remember: Only use on authorized systems!${NC}"
echo -e "${GREEN}Happy (ethical) hacking! 🔦${NC}"
echo ""

# Save installation info
cat > INSTALL_INFO.txt << EOF
Lume Security Toolkit - Installation Info
==========================================

Installation Date: $(date)
Installation Path: $PROJECT_DIR
Python Version: $(python3 --version)
Pip Version: $(pip3 --version)

Quick Commands:
  lume --version
  lume --list-tools
  lume --help

Documentation:
  cat $PROJECT_DIR/README.md

Uninstall:
  sudo pip3 uninstall lume-security-toolkit
  rm -rf $PROJECT_DIR
EOF

echo -e "${BLUE}Installation info saved to: $PROJECT_DIR/INSTALL_INFO.txt${NC}"
