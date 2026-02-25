#!/bin/bash

# Leadsec JobCard System - Frontend Setup Script

echo "Setting up LeadSec Frontend..."

# Check Node.js
echo "Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

# Install dependencies
echo "Installing frontend dependencies..."
npm install

echo ""
echo "✅ Frontend setup complete!"
echo ""
echo "Next steps:"
echo "1. Create .env file with VITE_API_URL=http://localhost:5000/api"
echo "2. Run: npm run dev"
echo ""
