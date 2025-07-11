from ultralytics import YOLO

model = YOLO("yolo10m.pt")

model.train(
    data="data.yaml",
    imgsz=640,
    epochs=100,
    batch=16,
    device="0",
    workers=4,
)
