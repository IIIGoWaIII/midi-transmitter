@echo off
echo Setting up MIDI receiver on Windows...

python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

echo Setup complete. Run with: venv\Scripts\python midi_receiver.py
pause
