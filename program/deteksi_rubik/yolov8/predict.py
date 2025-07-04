from ultralytics import YOLO

model = YOLO("best.pt")

model.predict(
    source="0",  # Use "0" for webcam, or provide a video file path
    show=True,  # Set to True to display the video with detections
    conf=0.85,  # Confidence threshold for detections
    show_labels=True,  # Show labels on detections
    show_conf=True,  # Show confidence scores on detections
    classes=[0, 1, 2, 3, 4, 6],  # Specify the classes to detect
)