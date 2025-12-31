import mido
import socket
import sys
import json

def main():
    if len(sys.argv) < 2:
        print("Usage: python midi_sender.py <WINDOWS_IP>")
        sys.exit(1)

    target_ip = sys.argv[1]
    target_port = 5005
    
    # Setup UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        print(f"Scanning for MIDI inputs...")
        inputs = mido.get_input_names()
        
        if not inputs:
            print("\n!!! ERROR: No MIDI inputs found !!!")
            print("Make sure your keyboard is plugged in and turned on.")
            print("You might need to install 'alsa-utils' and run 'aconnect -l' to debug.")
            input("\nPress Enter to exit...")
            sys.exit(1)

        print("-" * 30)
        print("Available MIDI inputs:")
        for i, name in enumerate(inputs):
            print(f"  [{i}] {name}")
        print("-" * 30)
        
        # Let user choose
        while True:
            try:
                choice = input(f"Select device [0-{len(inputs)-1}]: ").strip()
                idx = int(choice)
                if 0 <= idx < len(inputs):
                    input_name = inputs[idx]
                    break
                else:
                    print(f"Please enter a number between 0 and {len(inputs)-1}")
            except ValueError:
                print("Please enter a valid number")
        
        print(f"\nSelected: {input_name}")
        
        with mido.open_input(input_name) as port:
            print(f"\nSUCCESS: Listening on {input_name}")
            print(f"Sending to Windows at {target_ip}:{target_port}")
            print("Press Ctrl+C to stop.\n")
            
            for msg in port:
                if msg.type in ['note_on', 'note_off', 'control_change']:
                    data = {
                        'type': msg.type,
                        'note': getattr(msg, 'note', None),
                        'velocity': getattr(msg, 'velocity', None),
                        'control': getattr(msg, 'control', None),
                        'value': getattr(msg, 'value', None),
                        'channel': getattr(msg, 'channel', 0)
                    }
                    packet = json.dumps(data).encode('utf-8')
                    sock.sendto(packet, (target_ip, target_port))
                    # Subtle print to not flood terminal
                    if msg.type == 'note_on':
                        print(f"♪ Note {msg.note} ({msg.velocity})", end='\r')
    except KeyboardInterrupt:
        print("\n\nUser stopped the sender.")
    except Exception as e:
        print(f"\n!!! CRITICAL ERROR: {e} !!!")
        input("\nPress Enter to exit...")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
