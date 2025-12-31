#!/bin/bash
echo "Setting up MIDI sender on Fedora 43..."

# Install system dependencies
sudo dnf install -y python3-devel alsa-lib-devel gcc-c++

# Create virtual environment
python3 -m venv venv

# Install requirements
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

echo "Setup complete. Run with: ./venv/bin/python midi_sender.py <WINDOWS_IP>"
