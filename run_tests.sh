#!/bin/bash

# Flask User Management - Test Runner Script
# This script runs all pytest tests with proper configuration

set -e  # Exit on any error

echo "========================================="
echo "Flask User Management - Test Runner"
echo "========================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Error: Virtual environment not found"
    echo "Please run setup.sh first to create the environment"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows (Git Bash or similar)
    source .venv/Scripts/activate
else
    # Linux/Mac
    source .venv/bin/activate
fi
echo "✓ Virtual environment activated"
echo ""

# Check if pytest is installed
if ! python -c "import pytest" 2>/dev/null; then
    echo "❌ Error: pytest is not installed"
    echo "Installing pytest..."
    pip install pytest --quiet
    echo "✓ pytest installed"
fi
echo ""

# Clean up old test database
if [ -f "test.db" ]; then
    echo "🗑️  Cleaning up old test database..."
    rm test.db
    echo "✓ Test database cleaned"
fi
echo ""

# Run tests
echo "🧪 Running test suite..."
echo "========================================="
echo ""

# Run pytest with verbose output and capture all output
pytest test_app.py -v --tb=short --color=yes

# Capture exit code
TEST_EXIT_CODE=$?

echo ""
echo "========================================="

# Report results
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed successfully!"
    echo "========================================="
    echo ""
    
    # Count test results
    TOTAL_TESTS=$(pytest test_app.py --collect-only -q 2>/dev/null | grep -c "test_" || echo "unknown")
    echo "📊 Test Summary:"
    echo "   Total tests: $TOTAL_TESTS"
    echo "   Status: PASSED ✅"
    echo ""
else
    echo "❌ Some tests failed!"
    echo "========================================="
    echo ""
    echo "Please review the test output above for details."
    echo "Check defects.txt for known issues between README and implementation."
    echo ""
    exit 1
fi

# Cleanup test database after successful run
if [ -f "test.db" ]; then
    rm test.db
fi

echo "Next steps:"
echo "1. Review test results above"
echo "2. Check corrected_readme.md for accurate documentation"
echo "3. See defects.txt for all discovered issues"
echo ""
