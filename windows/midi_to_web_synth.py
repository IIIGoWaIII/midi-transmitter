import eventlet
eventlet.monkey_patch()

import socket
import json
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Flask & SocketIO Setup
app = Flask(__name__, template_folder='webui/templates')
app.config['SECRET_KEY'] = 'midi_secret'
# Using eventlet for proper WebSocket support and low latency
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

def handle_midi_message(data):
    msg_type = data.get('type')
    note = data.get('note')
    
    # Forward to WebUI
    print(f"Forwarding to WebUI: {msg_type} {note if note is not None else ''}")
    # socketio.emit on the instance broadcasts by default
    socketio.emit('midi_event', data)

def udp_listener():
    # Use eventlet-friendly socket if necessary, though monkey_patch usually handles it
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 5005))
    print("UDP Listener started on port 5005")
    while True:
        data, addr = sock.recvfrom(1024)
        try:
            msg = json.loads(data.decode('utf-8'))
            handle_midi_message(msg)
        except Exception as e:
            print(f"Error decoding MIDI message: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("WebUI client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("WebUI client disconnected")

@socketio.on('ui_midi_event')
def handle_ui_midi(data):
    handle_midi_message(data)

if __name__ == '__main__':
    # Start UDP listener using eventlet-friendly background task
    socketio.start_background_task(udp_listener)
    
    print("Starting MIDI-to-Web Bridge on http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000)
