#!/bin/bash

# Set the virtual environment directory
VENV_DIR="robotics"

# Check if the virtual environment directory exists
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment already exists."
else
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
    echo "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"

    # Install required packages
    pip install matplotlib
    pip install numpy
    pip install laspy
    pip install lazrs
fi

# Activate the virtual environment if it was created or exists
source "$VENV_DIR/bin/activate"

# Keep the terminal open
read -p "Press Enter to exit"
