#!/bin/bash

echo "╭──────────────────────────────────────────╮"
echo "│    نظام تحليل المشاعر - Emotion Detection    │"
echo "│    المصمم: عبدالله العويس                   │"
echo "╰──────────────────────────────────────────╯"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python is not installed"
    echo "Please install Python from https://www.python.org/downloads/"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

# Create and activate virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Make the script executable
chmod +x start.py

# Run the application
python3 start.py

# Deactivate virtual environment
deactivate
