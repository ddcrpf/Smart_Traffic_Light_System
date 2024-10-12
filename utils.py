import cv2

def init_camera_feed():
    # Initialize video capture from a camera or video file
    cap = cv2.VideoCapture(0)  # Replace '0' with video file path if needed
    if not cap.isOpened():
        print("Error: Could not open video feed.")
        exit()
    return cap
