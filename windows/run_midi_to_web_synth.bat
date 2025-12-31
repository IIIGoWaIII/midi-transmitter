@echo off
cd /d "%~dp0"
echo Starting MIDI-to-Web Synth Bridge...
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found! Please run setup_windows.bat first.
    pause
    exit /b
)
call venv\Scripts\activate.bat
python midi_to_web_synth.py
pause
