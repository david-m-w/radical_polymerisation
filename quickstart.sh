#!/bin/bash

# Exit on error
set -e

echo "Creating virtual environment..."
python3 -m venv .venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing requirements..."
pip install -r requirements.txt

echo "Setup complete!"
echo "To activate the environment, run: source .venv/bin/activate"
