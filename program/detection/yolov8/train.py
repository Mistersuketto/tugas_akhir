from ultralytics import YOLO

model = YOLO("yolov8m-seg.pt")

model.train(
    data="data.yaml",
    imgsz=640,
    epochs=300,
    batch=8,
    device="0",
    workers=4,
)
