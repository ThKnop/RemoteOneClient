import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# Initialisiere GStreamer
Gst.init(None)

def main():
    # Erstelle eine GStreamer-Pipeline
    pipeline = Gst.parse_launch(
        "v4l2src device=/dev/video0 ! "
        "image/jpeg, width=(int)1920, height=(int)1080, framerate=(fraction)30/1 ! "
        "jpegdec ! videoconvert ! omxh264enc ! h264parse ! "
        "rtph264pay config-interval=1 pt=96 ! "
        "udpsink host=192.168.200.110 port=5000"
    )

    # Setze die Pipeline auf "playing"
    pipeline.set_state(Gst.State.PLAYING)

    # Warte bis Fehler oder EOS
    bus = pipeline.get_bus()
    msg = bus.timed_pop_filtered(
        Gst.CLOCK_TIME_NONE,
        Gst.MessageType.ERROR | Gst.MessageType.EOS
    )

    # Fehlerbehandlung oder sauberes Beenden bei EOS
    if msg:
        if msg.type == Gst.MessageType.ERROR:
            err, debug = msg.parse_error()
            print("Error: %s" % err, debug)
        elif msg.type == Gst.MessageType.EOS:
            print("End of stream")

    # Setze die Pipeline auf "null"
    pipeline.set_state(Gst.State.NULL)

if __name__ == '__main__':
    main()
