#!/bin/bash

# Flask User Management Setup Script
# This script sets up the development environment and initializes the application

set -e  # Exit on error

echo "========================================"
echo "Flask User Management - Setup Script"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python3 found${NC}"
python3 --version

echo ""
echo "Step 1: Creating virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}✓ Virtual environment already exists${NC}"
fi

echo ""
echo "Step 2: Activating virtual environment..."
source .venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

echo ""
echo "Step 3: Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ Pip upgraded${NC}"

echo ""
echo "Step 4: Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt > /dev/null 2>&1
    echo -e "${GREEN}✓ Dependencies installed from requirements.txt${NC}"
else
    echo -e "${YELLOW}⚠ requirements.txt not found, installing manually...${NC}"
    pip install Flask==3.0.0 Flask-Login==0.6.3 Flask-WTF==1.2.1 WTForms==3.1.2 Werkzeug==3.0.1 email_validator==2.2.0 pytest > /dev/null 2>&1
    echo -e "${GREEN}✓ Dependencies installed${NC}"
fi

echo ""
echo "Step 5: Initializing database..."
python3 << EOF
import os
import sys
sys.path.insert(0, os.getcwd())
from app import app, init_db

with app.app_context():
    init_db(app)
    print("✓ Database initialized")
EOF

echo ""
echo "Step 6: Creating test user (optional)..."
python3 << EOF
import os
import sys
sys.path.insert(0, os.getcwd())
from app import app
from models import User, get_connection

with app.app_context():
    conn = get_connection(app)
    
    # Check if test user already exists
    existing = User.get_by_username(conn, 'testuser')
    if existing:
        print("✓ Test user already exists")
    else:
        User.create(conn, 'testuser', 'password123', 'test@example.com')
        print("✓ Test user created (username: testuser, password: password123)")
    
    conn.close()
EOF

echo ""
echo "========================================"
echo -e "${GREEN}Setup completed successfully!${NC}"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Activate the virtual environment (if not already):"
echo "     source .venv/bin/activate"
echo ""
echo "  2. Set environment variables (optional for development):"
echo "     export FLASK_SECRET=your-secret-key"
echo "     export FLASK_ENV=development"
echo ""
echo "  3. Run the application:"
echo "     python app.py"
echo ""
echo "  4. Open browser:"
echo "     http://localhost:5000"
echo ""
echo "  5. Login with test user:"
echo "     Username: testuser"
echo "     Password: password123"
echo "     Email: test@example.com"
echo ""
echo "  6. Run tests:"
echo "     pytest test_app.py -v"
echo ""
echo "For more information, see corrected_readme.md"
echo ""
