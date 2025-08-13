#!/bin/bash
# Unix/Linux/macOS script to run DevTerm

echo "Starting DevTerm..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the application
echo "Launching DevTerm..."
python main.py

# Check exit status
if [ $? -ne 0 ]; then
    echo ""
    echo "DevTerm exited with an error"
    read -p "Press Enter to continue..."
fi