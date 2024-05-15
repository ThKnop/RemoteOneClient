from flask import request, render_template, jsonify
import requests
from gstreamer.pipeline import create_pipeline, init_gstreamer
import logging

pipeline = None

def configure_routes(app):

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/start_stream', methods=['POST'])
    def start_stream():
        global pipeline
        local_delay_ms = int(request.form.get('local_delay_ms', 5000))
        target_ip = request.form.get('target_ip')
        video_port = int(request.form.get('video_port', 5000))

        if pipeline:
            pipeline.set_state(Gst.State.NULL)

        pipeline = create_pipeline(local_delay_ms, target_ip, video_port)
        if not pipeline:
            logging.error("Fehler beim Erstellen der Pipeline")
            return jsonify({"error": "Fehler beim Erstellen der Pipeline"}), 500

        pipeline.set_state(Gst.State.PLAYING)
        logging.info("Stream gestartet")
        return "Stream gestartet"

    @app.route('/stop_stream', methods=['POST'])
    def stop_stream():
        global pipeline
        if pipeline:
            pipeline.set_state(Gst.State.NULL)
            pipeline = None
        return "Stream gestoppt"

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

    init_gstreamer()
