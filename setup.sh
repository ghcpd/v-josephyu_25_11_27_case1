#!/bin/bash

# Flask User Management - Environment Setup Script
# This script sets up the complete development environment

set -e  # Exit on any error

echo "========================================="
echo "Flask User Management - Setup Script"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Error: Python is not installed or not in PATH"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

echo "✓ Found Python: $($PYTHON_CMD --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

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

# Upgrade pip
echo "⬆️  Upgrading pip..."
python -m pip install --upgrade pip --quiet
echo "✓ pip upgraded"
echo ""

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "📚 Installing dependencies from requirements.txt..."
    pip install -r requirements.txt --quiet
    echo "✓ Dependencies installed"
else
    echo "📚 Installing dependencies..."
    pip install flask flask-login flask-wtf wtforms email_validator pytest --quiet
    echo "✓ Dependencies installed"
fi
echo ""

# Clean up old database if it exists
if [ -f "app.db" ]; then
    echo "🗑️  Cleaning up old database..."
    rm app.db
    echo "✓ Old database removed"
fi

if [ -f "test.db" ]; then
    rm test.db
fi
echo ""

# Verify installation
echo "🔍 Verifying installation..."
python -c "import flask; import flask_login; import flask_wtf; import wtforms; import email_validator; import pytest" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ All required packages are properly installed"
else
    echo "❌ Error: Some packages failed to import"
    exit 1
fi
echo ""

# Display installed versions
echo "📋 Installed package versions:"
echo "   Flask: $(python -c 'import flask; print(flask.__version__)')"
echo "   Flask-Login: $(python -c 'import flask_login; print(flask_login.__version__)')"
echo "   Flask-WTF: $(python -c 'import flask_wtf; print(flask_wtf.__version__)')"
echo "   WTForms: $(python -c 'import wtforms; print(wtforms.__version__)')"
echo "   pytest: $(python -c 'import pytest; print(pytest.__version__)')"
echo ""

echo "========================================="
echo "✅ Setup completed successfully!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment (if not already active):"
echo "   - Windows: .venv\\Scripts\\activate"
echo "   - Linux/Mac: source .venv/bin/activate"
echo ""
echo "2. Run the application:"
echo "   python app.py"
echo ""
echo "3. Run tests:"
echo "   bash run_tests.sh"
echo "   or: pytest test_app.py -v"
echo ""
echo "4. Access the application:"
echo "   http://localhost:5000"
echo ""
