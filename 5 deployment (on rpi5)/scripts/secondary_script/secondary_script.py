import numpy as np
from modlib.apps import Annotator
from modlib.devices import AiCamera
from modlib.models import COLOR_FORMAT, MODEL_TYPE, Model
from modlib.models.post_processors import pp_od_yolo_ultralytics

class YOLO(Model):
    """YOLO model for IMX500 deployment."""

    def __init__(self):
        """Initialize the YOLO model for IMX500 deployment."""
        super().__init__(
            model_file="files/packerOut.zip",  # replace with proper directory
            model_type=MODEL_TYPE.CONVERTED,
            color_format=COLOR_FORMAT.RGB,
            preserve_aspect_ratio=False,
        )

        self.labels = np.genfromtxt(
            "files/labels.txt",  # replace with proper directory
            dtype=str,
            delimiter="\n",
            ndmin = 1
        )

    def post_process(self, output_tensors):
        """Post-process the output tensors for object detection."""
        return pp_od_yolo_ultralytics(output_tensors)

device = AiCamera(frame_rate=26)  # Optimal frame rate for maximum FPS of the YOLO model running on the AI Camera
model = YOLO()
device.deploy(model)

annotator = Annotator()

with device as stream:
    for frame in stream:
        detections = frame.detections[frame.detections.confidence > 0.55]
        labels = [f"{model.labels[class_id]}: {score:0.2f}" for _, score, class_id, _ in detections]

        annotator.annotate_boxes(frame, detections, labels=labels, alpha=0.3, corner_radius=10)
        frame.display()
