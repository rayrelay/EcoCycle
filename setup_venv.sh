#!/bin/bash

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies (if any)
# pip install pytest pytest-flask coverage

echo "Virtual environment setup complete. Activate with: source venv/bin/activate"