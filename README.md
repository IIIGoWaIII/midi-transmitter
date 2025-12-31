# MIDI Transmitter

A cross-platform (Linux to Windows) MIDI transmission system. This project allows you to capture MIDI input on a Linux machine (e.g., from a digital piano) and transmit it over a local network to a Windows machine, which then plays the sounds via a Web-based synthesizer.

## Architecture

- **Linux Transmitter**: Uses `mido` to listen for MIDI events and sends them as JSON over UDP.
- **Windows Receiver/Synth**: A Flask-SocketIO server that receives UDP packets and forwards them to a WebUI using WebSockets. The WebUI (using `soundfont-player`) synthesizes the audio.

## Setup

### Windows (Receiver & Synth)

1. Navigate to the `windows` directory.
2. Run `setup_windows.bat` to create a virtual environment and install dependencies.
3. Run `run_midi_to_web_synth.bat` to start the server.
4. Open a web browser at `http://localhost:5000` (it should open automatically).

### Linux (Transmitter)

1. Navigate to the `linux` directory.
2. Run `setup_fedora.sh` (or install `mido` and `python3-rtmidi` manually).
3. Run `run_sender.sh` to start transmitting. You will be prompted to select your MIDI input device.

## Requirements

- Python 3.x
- Network connectivity between the Linux and Windows machines.
- (Windows) Flask, Flask-SocketIO, Eventlet.
- (Linux) Mido, python-rtmidi.

## License

MIT
