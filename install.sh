#!/bin/bash
# Lume Security Toolkit - Quick Installer for Kali Linux
# This script installs Lume and all dependencies

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║           🔦 LUME SECURITY TOOLKIT 🔦                    ║"
echo "║                                                          ║"
echo "║           Quick Installer for Kali Linux                ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}Error: This installer is designed for Linux systems${NC}"
    exit 1
fi

# Check Python version
echo -e "${YELLOW}[1/6] Checking Python version...${NC}"
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.8"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
else
    echo -e "${RED}✗ Python 3.8+ required. Found: $PYTHON_VERSION${NC}"
    echo "Install Python 3.8+: sudo apt install python3 python3-pip"
    exit 1
fi

# Check pip
echo -e "${YELLOW}[2/6] Checking pip...${NC}"
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓ pip3 found${NC}"
else
    echo -e "${RED}✗ pip3 not found${NC}"
    echo "Installing pip3..."
    sudo apt update
    sudo apt install python3-pip -y
fi

# Check pentesting tools
echo -e "${YELLOW}[3/6] Checking pentesting tools...${NC}"
TOOLS=("nmap" "gobuster" "nikto" "sqlmap" "hydra" "msfconsole" "whatweb")
MISSING_TOOLS=()

for tool in "${TOOLS[@]}"; do
    if command -v $tool &> /dev/null; then
        echo -e "${GREEN}✓ $tool found${NC}"
    else
        echo -e "${YELLOW}⚠ $tool not found${NC}"
        MISSING_TOOLS+=($tool)
    fi
done

if [ ${#MISSING_TOOLS[@]} -gt 0 ]; then
    echo -e "${YELLOW}Missing tools: ${MISSING_TOOLS[*]}${NC}"
    read -p "Install missing tools? [y/N]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Installing tools..."
        sudo apt update
        sudo apt install nmap gobuster nikto sqlmap hydra metasploit-framework whatweb -y
    fi
fi

# Install Lume
echo -e "${YELLOW}[4/6] Installing Lume Security Toolkit...${NC}"
if [ -f "setup.py" ]; then
    sudo pip3 install -e .
    echo -e "${GREEN}✓ Lume installed successfully${NC}"
else
    echo -e "${RED}✗ setup.py not found. Are you in the project directory?${NC}"
    exit 1
fi

# Verify installation
echo -e "${YELLOW}[5/6] Verifying installation...${NC}"
if command -v lume &> /dev/null; then
    echo -e "${GREEN}✓ lume command available${NC}"
    lume --version
else
    echo -e "${RED}✗ lume command not found${NC}"
    echo "Try adding to PATH: export PATH=\$PATH:~/.local/bin"
    exit 1
fi

# Run tests
echo -e "${YELLOW}[6/6] Running tests...${NC}"
if [ -f "test_lume.sh" ]; then
    chmod +x test_lume.sh
    ./test_lume.sh
else
    echo -e "${YELLOW}⚠ test_lume.sh not found, skipping tests${NC}"
fi

# Success message
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║              ✅ INSTALLATION COMPLETE! ✅                 ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${CYAN}Quick Start:${NC}"
echo "  lume --version              # Check version"
echo "  lume --list-tools           # List supported tools"
echo "  lume --dry-run \"scan ports on 192.168.1.1\""
echo "  lume \"scan ports on scanme.nmap.org\""
echo ""
echo -e "${CYAN}Documentation:${NC}"
echo "  cat QUICKSTART.md           # Quick start guide"
echo "  cat README.md               # Full documentation"
echo "  ./demo.sh                   # Interactive demo"
echo ""
echo -e "${YELLOW}Remember: Only use on authorized systems!${NC}"
echo -e "${GREEN}Happy (ethical) hacking! 🔦${NC}"
