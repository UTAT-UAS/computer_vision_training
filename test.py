import cv2
import os
from ultralytics import YOLO


def main():
    # Load the custom trained model
    # By default, YOLO saves the best model during training to runs/train/<name>/weights/best.pt
    model_path = "runs/detect/runs/train/yolo26n/weights/best.pt"

    print(f"Loading model: {model_path}")
    model = YOLO(model_path)

    print(
        "Starting webcam... Press 'q' (with window in focus) or Ctrl+C in terminal to stop."
    )

    results = model.predict(source=0, show=True, stream=True, conf=0.2)

    # We must iterate through the generator to keep the stream running and frames updating
    for _ in results:
        pass


if __name__ == "__main__":
    main()
