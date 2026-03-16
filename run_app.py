import subprocess
import webbrowser
import time

print("Starting Flight Delay Prediction Application...")
print("=" * 60)

# Start Flask app in background
proc = subprocess.Popen(['python', 'app.py'], 
                       cwd=r'c:\Users\gulam\OneDrive\Desktop\IO Mini Project\flight-delay-webapp')

print("\nWaiting for server to start...")
time.sleep(3)

print("\nOpening browser at http://localhost:5000")
webbrowser.open('http://localhost:5000')

print("\nApplication is running!")
print("Press Ctrl+C to stop the server")
print("=" * 60)

try:
    proc.wait()
except KeyboardInterrupt:
    print("\nShutting down...")
    proc.terminate()
