#!/bin/bash
# Demo script for Lume Security Toolkit
# Shows various usage examples in dry-run mode (safe to execute)

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         Lume Security Toolkit - Interactive Demo          ║"
echo "║         Think in English. Hack in Kali.                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

pause() {
    echo ""
    read -p "Press Enter to continue..."
    echo ""
}

demo_command() {
    local description=$1
    local command=$2
    
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}Demo: $description${NC}"
    echo -e "${YELLOW}Command: $command${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    eval "$command"
    pause
}

# Check if lume is installed
if ! command -v lume &> /dev/null; then
    echo "ERROR: lume is not installed"
    echo "Please run: sudo pip3 install -e ."
    exit 1
fi

echo "This demo shows Lume's capabilities using --dry-run mode"
echo "(No actual commands will be executed)"
pause

# Demo 1: Port Scanning
demo_command \
    "Port Scanning" \
    "lume --dry-run 'scan ports on 192.168.1.1'"

# Demo 2: Directory Enumeration
demo_command \
    "Directory Enumeration" \
    "lume --dry-run 'find admin login page on example.com'"

# Demo 3: Web Vulnerability Scanning
demo_command \
    "Web Vulnerability Scanning" \
    "lume --dry-run 'scan web vulnerabilities on https://testsite.com'"

# Demo 4: SQL Injection Testing
demo_command \
    "SQL Injection Testing" \
    "lume --dry-run 'test sql injection on http://target.com/page?id=1'"

# Demo 5: Subdomain Enumeration
demo_command \
    "Subdomain Enumeration" \
    "lume --dry-run 'find subdomains of example.com'"

# Demo 6: Network Discovery
demo_command \
    "Network Discovery" \
    "lume --dry-run 'find live hosts on 192.168.1.0'"

# Demo 7: Brute Force
demo_command \
    "SSH Brute Force" \
    "lume --dry-run 'brute force ssh on 192.168.1.10'"

# Demo 8: OS Detection
demo_command \
    "OS Detection" \
    "lume --dry-run 'detect operating system on 192.168.1.50'"

# Demo 9: List Tools
demo_command \
    "List Supported Tools" \
    "lume --list-tools"

echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                    Demo Complete!                          ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "To use Lume for real:"
echo "  1. Remove --dry-run flag"
echo "  2. Ensure you have authorization"
echo "  3. Confirm execution when prompted"
echo ""
echo "Example: lume 'scan ports on scanme.nmap.org'"
echo ""
