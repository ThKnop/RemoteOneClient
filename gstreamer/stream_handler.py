# stream_handler.py

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import logging

# Initialisiere GStreamer und die GObject Thread-Unterstützung
def init_gstreamer():
    Gst.init(None)

# Erstelle eine GStreamer-Pipeline mit den gegebenen Parametern
def create_pipeline(local_delay_ms, target_ip, video_port):
    print("create Pipeline")
    pipeline = Gst.parse_launch(
        f"v4l2src device=/dev/video0 ! "
        f"image/jpeg, width=(int)1920, height=(int)1080, framerate=(fraction)30/1 ! "
        f"jpegdec ! videoconvert ! omxh264enc ! h264parse ! "
        f"rtph264pay config-interval=1 pt=96 ! "
        f"udpsink host={target_ip} port={video_port}"
    )
    return pipeline

# Globale Variable, um die Pipeline-Instanz zu speichern
pipeline = None

def start_stream(local_delay_ms, target_ip, video_port):
    global pipeline
    if pipeline:
        pipeline.set_state(Gst.State.NULL)  # Setze die aktuelle Pipeline auf NULL, falls bereits eine existiert

    pipeline = create_pipeline(local_delay_ms, target_ip, video_port)
    if not pipeline:
        logging.error("Fehler beim Erstellen der Pipeline")
        return False, "Fehler beim Erstellen der Pipeline"

    pipeline.set_state(Gst.State.PLAYING)
    logging.info("Stream gestartet")
    return True, "Stream gestartet"

def stop_stream():
    global pipeline
    if pipeline:
        pipeline.set_state(Gst.State.NULL)  # Stoppe die Pipeline
        pipeline = None
        logging.info("Stream gestoppt")
        return "Stream gestoppt"
    return "Kein Stream zum Stoppen vorhanden"

# Initialisiere das Logging-System
logging.basicConfig(level=logging.INFO)
