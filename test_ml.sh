#!/bin/bash
# Test script for ML normalization feature

echo "========================================="
echo "Lume ML Feature Test Suite"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test counter
TESTS=0
PASSED=0
FAILED=0

# Function to run test
run_test() {
    local test_name="$1"
    local command="$2"
    
    TESTS=$((TESTS + 1))
    echo -e "${YELLOW}Test $TESTS: $test_name${NC}"
    echo "Command: $command"
    echo ""
    
    # Run command (dry-run mode to avoid actual execution)
    if eval "$command --dry-run" 2>&1 | grep -q "Command"; then
        echo -e "${GREEN}✓ PASSED${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗ FAILED${NC}"
        FAILED=$((FAILED + 1))
    fi
    echo ""
    echo "-----------------------------------------"
    echo ""
}

# Check if lume is installed
if ! command -v lume &> /dev/null; then
    echo -e "${RED}Error: lume command not found${NC}"
    echo "Please install Lume first:"
    echo "  sudo pip3 install -e . --break-system-packages"
    exit 1
fi

# Check if spaCy is available
echo "Checking spaCy installation..."
if python3 -c "import spacy; spacy.load('en_core_web_sm')" 2>/dev/null; then
    echo -e "${GREEN}✓ spaCy is installed${NC}"
    ML_AVAILABLE=true
else
    echo -e "${YELLOW}⚠ spaCy not available - ML tests will be skipped${NC}"
    echo "Install with:"
    echo "  sudo pip3 install spacy --break-system-packages"
    echo "  python -m spacy download en_core_web_sm"
    ML_AVAILABLE=false
fi
echo ""
echo "========================================="
echo ""

# Test 1: Basic rule-based parsing (no ML)
run_test "Basic port scan (rule-based)" \
    'lume "scan ports on 192.168.1.1"'

# Test 2: Directory enumeration (rule-based)
run_test "Directory enumeration (rule-based)" \
    'lume "find directories on example.com"'

# Test 3: SQL injection (rule-based)
run_test "SQL injection test (rule-based)" \
    'lume "test sql injection on http://target.com/page?id=1"'

if [ "$ML_AVAILABLE" = true ]; then
    echo ""
    echo "========================================="
    echo "ML-Enhanced Tests"
    echo "========================================="
    echo ""
    
    # Test 4: ML normalization - flexible phrasing
    run_test "ML: Flexible phrasing" \
        'lume --ml-normalize "first give ip 192.168.1.1 then scan"'
    
    # Test 5: ML normalization - synonym handling
    run_test "ML: Synonym handling" \
        'lume --ml-normalize "enumerate admin pages on example.com"'
    
    # Test 6: ML normalization - word order variation
    run_test "ML: Word order variation" \
        'lume --ml-normalize "check 192.168.1.1 for open ports"'
    
    # Test 7: ML with custom confidence
    run_test "ML: Custom confidence threshold" \
        'lume --ml-normalize --ml-confidence 0.60 "scan target.com"'
    
    # Test 8: ML fallback (low confidence)
    run_test "ML: Low confidence fallback" \
        'lume --ml-normalize "do something with 192.168.1.1"'
fi

# Test 9: Explain mode
run_test "Explain mode" \
    'lume --explain "scan ports on 192.168.1.1"'

# Test 10: Version check
echo -e "${YELLOW}Test $((TESTS + 1)): Version check${NC}"
TESTS=$((TESTS + 1))
if lume --version | grep -q "0.3.0"; then
    echo -e "${GREEN}✓ PASSED - Version 0.3.0 detected${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}✗ FAILED - Expected version 0.3.0${NC}"
    FAILED=$((FAILED + 1))
fi
echo ""
echo "-----------------------------------------"
echo ""

# Summary
echo "========================================="
echo "Test Summary"
echo "========================================="
echo "Total Tests: $TESTS"
echo -e "${GREEN}Passed: $PASSED${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}Failed: $FAILED${NC}"
else
    echo -e "${GREEN}Failed: $FAILED${NC}"
fi
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    exit 1
fi
