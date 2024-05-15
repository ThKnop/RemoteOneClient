import gi
from gi.repository import Gst, GObject

gi.require_version('Gst', '1.0')

def init_gstreamer():
    Gst.init(None)
    GObject.threads_init()

def create_pipeline(local_delay_ms, target_ip, video_port):
    pipeline_desc = (
        f"v4l2src device=/dev/video0 ! "
        f"'image/jpeg,width=1920,height=1080,framerate=30/1' ! "
        f"jpegdec ! nvvidconv ! "
        f"'video/x-raw(memory:NVMM), format=(string)NV12' ! "
        f"omxh264enc ! h264parse ! "
        f"tee name=t "
        f"t. ! queue ! rtph264pay config-interval=1 pt=96 ! "
        f"udpsink host={target_ip} port={video_port} sync=false "
        f"t. ! queue max-size-time={(local_delay_ms * 1000000)} ! "
        f"videoconvert ! autovideosink sync=true"
    )
    pipeline = Gst.parse_launch(pipeline_desc)
    return pipeline
