#!/usr/bin/env python

import sys, os

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from src import train_model  # Import the module

def main():
    train_model.main(optimize=True)  # Call the main() function defined in train_model.py

if __name__ == "__main__":
    main()
