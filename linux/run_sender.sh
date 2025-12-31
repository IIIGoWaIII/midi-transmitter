#!/bin/bash

# === CONFIGURE THIS ===
WINDOWS_IP="192.168.1.11"
# ======================

echo "Starting MIDI Sender to $WINDOWS_IP..."
./venv/bin/python midi_sender.py "$WINDOWS_IP"

echo ""
read -p "Press Enter to close terminal..."
