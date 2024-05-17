from flask import Flask, request, render_template, jsonify, redirect, url_for
import requests
import logging
from gstreamer.stream_handler import init_gstreamer, start_stream, stop_stream, get_stream_stats

app = Flask(__name__)

def configure_routes(app):

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/configure_master', methods=['POST'])
    def configure_master():
        return render_template('configure_master.html')

    @app.route('/start_stream', methods=['POST'])
    def start_stream_route():
        local_delay_ms = int(request.form.get('local_delay_ms', 5000))
        target_ip = request.form.get('target_ip', '192.168.200.110')
        video_port = int(request.form.get('video_port', 5000))
        success, message = start_stream(local_delay_ms, target_ip, video_port)
        if not success:
            return jsonify({"error": message}), 500
        return render_template('remote.html')

    @app.route('/stop_stream', methods=['POST'])
    def stop_stream_route():
        message = stop_stream()
        return redirect(url_for('index'))

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

    @app.route('/stream_stats', methods=['GET'])
    def stream_stats_route():
        stats = get_stream_stats()
        logging.info(f"Stats: {stats}")
        return jsonify(stats)

    init_gstreamer()
