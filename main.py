from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.pt")


# Train the model
model.train(
    data="config.yaml",  # path to dataset YAML
    epochs=65,  # number of training epochs
)


