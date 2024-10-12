from ultralytics import YOLO  # Corrected import
from emissions_model import predict_emission

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

def process_frame(frame):
    # Perform detection using YOLOv8
    results = model.detect(frame)

    car_count = 0
    total_emission = 0
    emergency_vehicle_detected = False

    # Iterate over detected objects
    for obj in results['detections']:
        vehicle_type = obj['label']
        if vehicle_type in ['car', 'truck', 'motorcycle', 'bus']:
            car_count += 1
            total_emission += predict_emission(vehicle_type)
        if vehicle_type == 'emergency':
            emergency_vehicle_detected = True

    return car_count, total_emission, emergency_vehicle_detected
