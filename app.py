from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_stream', methods=['POST'])
def start_stream():
    command = "gst-launch-1.0 v4l2src device=/dev/video0 ! 'image/jpeg, width=(int)1920, height=(int)1080, framerate=(fraction)30/1' ! jpegdec ! videoconvert ! omxh264enc ! h264parse ! rtph264pay config-interval=1 pt=96 ! udpsink host=192.168.200.110 port=5000"

    try:
        subprocess.Popen(command, shell=True)
        return 'Stream gestartet!'
    except Exception as e:
        return f'Fehler beim Starten des Streams: {str(e)}'

@app.route('/stop_stream', methods=['POST'])
def stop_stream():
    # Hier könnte der Code stehen, um den Stream zu stoppen
    return 'Stream gestoppt!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

