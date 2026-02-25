#!/bin/bash

# Leadsec JobCard System - Complete Setup Script

echo "Setting up Leadsec JobCard System..."

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check MySQL
echo "Checking MySQL installation..."
if ! command -v mysql &> /dev/null; then
    echo "MySQL is not installed. Please install MySQL 5.7 or higher."
    exit 1
fi

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Copy .env file
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration"
fi

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your database and email credentials"
echo "2. Run: python create_db.py (to create MySQL database)"
echo "3. Run: python run.py (to start the API)"
echo ""
