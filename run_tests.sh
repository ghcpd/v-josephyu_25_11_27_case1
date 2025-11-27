#!/bin/bash

# Test Runner Script for Flask User Management Application
# Runs all tests with pytest and generates coverage report

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "========================================"
echo "Flask User Management - Test Runner"
echo "========================================"
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}⚠ Virtual environment not activated${NC}"
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

echo -e "${GREEN}✓ Using Python from: $VIRTUAL_ENV${NC}"
python --version
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}Error: pytest is not installed${NC}"
    echo "Installing pytest..."
    pip install pytest pytest-cov > /dev/null 2>&1
    echo -e "${GREEN}✓ pytest installed${NC}"
fi

echo ""
echo "========================================"
echo "Running Unit Tests"
echo "========================================"
echo ""

# Run tests with verbose output
if [ "$1" == "--coverage" ] || [ "$1" == "-c" ]; then
    echo "Running tests with coverage report..."
    echo ""
    pytest test_app.py -v --cov=. --cov-report=html --cov-report=term-missing
    
    echo ""
    echo -e "${GREEN}Coverage report generated in htmlcov/index.html${NC}"
else
    pytest test_app.py -v
fi

TEST_RESULT=$?

echo ""
echo "========================================"
if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
else
    echo -e "${RED}✗ Some tests failed${NC}"
fi
echo "========================================"
echo ""

# Additional test statistics
echo "Test Summary:"
python3 << EOF
import subprocess
import re

result = subprocess.run(['pytest', 'test_app.py', '--collect-only', '-q'], 
                       capture_output=True, text=True)
output = result.stdout
lines = output.strip().split('\n')
print(f"Total test items: {len(lines) - 1}")
EOF

echo ""
echo "Common testing commands:"
echo "  Run all tests:"
echo "    bash run_tests.sh"
echo ""
echo "  Run with coverage:"
echo "    bash run_tests.sh --coverage"
echo ""
echo "  Run specific test class:"
echo "    pytest test_app.py::TestUserModel -v"
echo ""
echo "  Run specific test:"
echo "    pytest test_app.py::TestUserModel::test_user_creation -v"
echo ""
echo "  Run tests with output:"
echo "    pytest test_app.py -v -s"
echo ""

exit $TEST_RESULT
