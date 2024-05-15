from flask import Flask, request, render_template, jsonify
import requests
import logging
from gstreamer.stream_handler import init_gstreamer, start_stream, stop_stream

app = Flask(__name__)

def configure_routes(app):

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/start_stream', methods=['POST'])
    def start_stream_route():
        local_delay_ms = int(request.form.get('local_delay_ms', 5000))
        target_ip = request.form.get('target_ip', '192.168.200.110')  # Standardwert als Beispiel
        video_port = int(request.form.get('video_port', 5000))  # Standardwert als Beispiel
        success, message = start_stream(local_delay_ms, target_ip, video_port)
        if not success:
            return jsonify({"error": message}), 500
        return message

    @app.route('/stop_stream', methods=['POST'])
    def stop_stream_route():
        message = stop_stream()
        return message

    @app.route('/configure_slave', methods=['POST'])
    def configure_slave():
        slave_ip = request.form.get('slave_ip')
        action = request.form.get('action')
        data = {
            'local_delay_ms': request.form.get('local_delay_ms'),
            'target_ip': request.form.get('target_ip'),
            'video_port': request.form.get('video_port')
        }
        response = requests.post(f'http://{slave_ip}:8080/{action}', data=data)
        return response.text

    # Diese Zeile initialisiert GStreamer beim Starten der Flask-Anwendung
    init_gstreamer()
