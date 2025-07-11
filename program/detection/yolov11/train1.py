from ultralytics import YOLO

model = YOLO("yolo11m.pt")

model.train(
    data="data.yaml",
    imgsz=640,
    epochs=100,
    batch=16,
    device="cpu",
    workers=4,
)