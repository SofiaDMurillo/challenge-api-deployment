#!/bin/bash

# Make this file executable: chmod +x run-main.sh
# Run it with: ./run-main.sh

clear

# === Define color codes ===
BLUE_BG="\033[44m"
GREEN_BG="\033[42m"
RED_BG="\033[41m"
WHITE_TEXT="\033[97m"
BLACK_TEXT="\033[30m"
RESET="\033[0m"

# === Define print helpers ===
print_blue() {
    echo ""
    echo -e "${BLUE_BG}${WHITE_TEXT}>>> $1${RESET}"
    echo ""
}

print_green() {
    echo ""
    echo -e "${GREEN_BG}${WHITE_TEXT}>>> $1${RESET}"
    echo ""
}

print_error() {
    echo ""
    echo -e "${RED_BG}${WHITE_TEXT}>>> ERROR: $1${RESET}"
    echo ""
    exit 1
}

# === Navigate to script directory ===
cd "$(dirname "$0")"

# === Activate virtual environment ===
print_blue "Activating virtual environment..."
source .venv/Scripts/activate || print_error "Failed to activate .venv. Are you in Git Bash or WSL?"

# === Show Python version ===
print_blue "Using Python version:"
python --version

# === Run training script ===
print_blue "Running model training via src/main.py..."
python src/main.py || print_error "Python script failed."

# === Done ===
print_green "Model training finished successfully."
