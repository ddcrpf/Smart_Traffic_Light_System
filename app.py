import cv2
import time
from vehicle_detection import process_frame
from traffic_control import control_traffic_lights
from utils import init_camera_feed

# Set up video feed (camera or video file)
cap = init_camera_feed()

# Main loop to capture frames and process them
def main():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Process the current frame for vehicle detection
        car_count, total_emission, emergency_vehicle_detected = process_frame(frame)

        # Control traffic lights based on detection
        control_traffic_lights(car_count, total_emission, emergency_vehicle_detected)

        # Display the current frame (optional)
        cv2.imshow('Traffic Camera', frame)

        # Wait for 5 seconds before capturing the next frame
        time.sleep(5)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
