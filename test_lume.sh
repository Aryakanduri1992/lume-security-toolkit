#!/bin/bash
# Test script for Lume Security Toolkit

echo "==================================="
echo "Lume Security Toolkit - Test Suite"
echo "==================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Test function
test_command() {
    local description=$1
    local command=$2
    
    echo -n "Testing: $description... "
    
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}PASSED${NC}"
        ((PASSED++))
    else
        echo -e "${RED}FAILED${NC}"
        ((FAILED++))
    fi
}

# Check if lume is installed
echo "Checking installation..."
if ! command -v lume &> /dev/null; then
    echo -e "${RED}ERROR: lume command not found${NC}"
    echo "Please install first: sudo pip3 install -e ."
    exit 1
fi
echo -e "${GREEN}lume is installed${NC}"
echo ""

# Basic tests
echo "Running basic tests..."
test_command "Version flag" "lume --version"
test_command "Help flag" "lume --help"
test_command "List tools" "lume --list-tools"
echo ""

# Dry-run tests (safe to run)
echo "Running dry-run tests..."
test_command "Port scan dry-run" "lume --dry-run 'scan ports on 192.168.1.1' | grep -q 'nmap'"
test_command "Directory enum dry-run" "lume --dry-run 'find admin page on example.com' | grep -q 'gobuster'"
test_command "Web scan dry-run" "lume --dry-run 'scan web vulnerabilities on example.com' | grep -q 'nikto'"
test_command "SQL injection dry-run" "lume --dry-run 'test sql injection on http://test.com' | grep -q 'sqlmap'"
test_command "Subdomain enum dry-run" "lume --dry-run 'find subdomains of example.com' | grep -q 'gobuster'"
echo ""

# Target extraction tests
echo "Running target extraction tests..."
test_command "IP extraction" "lume --dry-run 'scan 192.168.1.100' | grep -q '192.168.1.100'"
test_command "Domain extraction" "lume --dry-run 'scan example.com' | grep -q 'example.com'"
test_command "URL extraction" "lume --dry-run 'scan https://example.com' | grep -q 'https://example.com'"
echo ""

# Summary
echo "==================================="
echo "Test Results:"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo "==================================="

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${YELLOW}Some tests failed. Please review.${NC}"
    exit 1
fi
