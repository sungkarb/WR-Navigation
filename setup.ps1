$VENV_DIR = "robotics"

# Check if the virtual environment directory exists
if (Test-Path $VENV_DIR) {
    Write-Host "Virtual environment already exists."
} else {
    Write-Host "Creating virtual environment..."
    python -m venv $VENV_DIR
    Write-Host "Activating virtual environment..."
    & "$VENV_DIR\Scripts\Activate.ps1"

    # Install required packages
    pip install matplotlib
    pip install numpy
    pip install laspy
    pip install lazrs
}

# Activate the virtual environment if it was created
& "$VENV_DIR\Scripts\Activate.ps1"

# Keep the window open
Read-Host "Press Enter to exit"