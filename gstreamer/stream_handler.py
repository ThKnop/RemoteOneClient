import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject
import logging

# Initialisiere GStreamer und die GObject Thread-Unterstützung
def init_gstreamer():
    Gst.init(None)
    GObject.threads_init()

# Erstelle eine GStreamer-Pipeline mit den gegebenen Parametern
def create_pipeline(local_delay_ms, target_ip, video_port):
    # pipeline = Gst.parse_launch(
    #     f"v4l2src device=/dev/video0 ! "
    #     f"image/jpeg, width=(int)1920, height=(int)1080, framerate=(fraction)30/1 ! "
    #     f"jpegdec ! videoconvert ! omxh264enc ! h264parse ! "
    #     f"rtph264pay config-interval=1 pt=96 ! "
    #     f"udpsink host={target_ip} port={video_port}"
    # )

    video = "/home/thomas/RemoteOneClient/Mum_S3E06_018_25fps_720p.mp4"

    pipeline = Gst.parse_launch(
        f"filesrc location={video} ! "
        f"qtdemux name=demux demux.video_0 ! "
        f"queue ! h264parse ! rtph264pay config-interval=1 pt=96 ! "
        f"udpsink host={target_ip} port={video_port}"
    )

    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message", bus_call)
    return pipeline

# Globale Variable, um die Pipeline-Instanz zu speichern
pipeline = None
stream_stats = {
    'bitrate': 0,
    'jitter': 0,
    'latency': 0
}

def bus_call(bus, message):
    global stream_stats
    logging.info(f"Received message: {message.type}")
    t = message.type
    if t == Gst.MessageType.ELEMENT:
        struct = message.get_structure()
        logging.info(f"Message structure: {struct.get_name()}")
        if struct.has_name("GstUDPSinkStats"):
            stream_stats['bitrate'] = struct.get_double("bitrate")[1]
            stream_stats['jitter'] = struct.get_double("jitter")[1]
            stream_stats['latency'] = struct.get_double("latency")[1]
            logging.info(f"Updated stats: {stream_stats}")

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

def get_stream_stats():
    return stream_stats

# Initialisiere das Logging-System
logging.basicConfig(level=logging.INFO)
