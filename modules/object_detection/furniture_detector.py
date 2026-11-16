
from ultralytics import YOLO
from PIL import Image
import numpy as np


# Load lightweight YOLO model
model = YOLO("yolov8n.pt")


def detect_furniture(image):
    """
    Detect furniture and common objects in a room image.
    Uses YOLOv8 Nano on CPU.
    """

    if isinstance(image, Image.Image):
        image_array = np.array(image.convert("RGB"))
    else:
        image_array = np.array(image)

    # Run object detection on CPU
    results = model.predict(
        source=image_array,
        device="cpu",
        conf=0.15,
        verbose=False
    )

    detected_objects = []

    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            object_name = model.names[class_id].replace("_", " ").strip().lower()

            if object_name == "pottedplant":
                object_name = "potted plant"

            detected_objects.append({
                "name": object_name,
                "confidence": round(confidence * 100, 2),
                "class_id": class_id
            })

    # Generate image with detection boxes
    annotated_image = results[0].plot()

    # Convert BGR to RGB
    annotated_image = annotated_image[:, :, ::-1]

    return {
        "detected_objects": detected_objects,
        "annotated_image": Image.fromarray(annotated_image)
    }
