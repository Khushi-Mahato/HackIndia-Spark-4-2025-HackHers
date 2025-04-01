#!/bin/bash

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    echo "Please enter your Gemini API key:"
    read API_KEY
    echo "GEMINI_API_KEY=$API_KEY" > .env
fi

# Start the server
echo "Starting server..."
echo ""
echo "When the server is running, open http://localhost:8000/demo.html in your browser"
echo ""
echo "Press Ctrl+C to stop the server when you're done"
python src/main.py 