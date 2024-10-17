from flask import Flask, render_template, Response, request, session, redirect, url_for
import cv2
from ultralytics import YOLO

# Flask app setup
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulated database of users
users = {
    "policeman": {"password": "police123", "role": "policeman"},
    "admin": {"password": "admin123", "role": "admin"}
}

# Load the YOLOv8 model
model = YOLO('final_yolo_finetuned.pt')

# Emission mapping (as defined earlier)
emission_mapping = {
    'auto': 60,
    'bus': 900,
    'tempo': 150,
    'tractor': 1000,
    'truck': 1300
}

# Global variable to store the latest model decision
traffic_light_decision = 'red'

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists and password is correct
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('control_panel'))
        else:
            return "Invalid credentials, please try again."
    
    return render_template('login.html')

# Control panel (traffic control) route
@app.route('/control', methods=['GET', 'POST'])
def control_panel():
    global traffic_light_decision
    
    if 'username' not in session:
        return redirect(url_for('login'))
    
    role = session.get('role')
    
    if request.method == 'POST':
        override_light = request.form.get('traffic_light')
        if override_light:
            traffic_light_decision = override_light
            return f"Traffic light manually set to: {traffic_light_decision}"
    
    # Render the control panel with the model's decision
    return render_template('control_panel.html', model_decision=traffic_light_decision, role=role)

# Live video feed route
def generate_frames():
    global traffic_light_decision

    camera = cv2.VideoCapture(0)  # Capture video from webcam (index 0)

    while True:
        # Capture frame-by-frame
        success, frame = camera.read()
        if not success:
            break
        else:
            # Convert frame to RGB for YOLO model processing
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Perform detection using the fine-tuned YOLO model
            results = model(frame_rgb)

            # Count vehicle types detected
            vehicle_counts = {
                'auto': 0,
                'bus': 0,
                'tempo': 0,
                'tractor': 0,
                'truck': 0
            }
            for result in results:
                for cls in result.boxes.cls:
                    label = model.names[int(cls)]
                    if label in vehicle_counts:
                        vehicle_counts[label] += 1

            # Calculate total emissions
            total_emissions = calculate_emissions(vehicle_counts)

            # Simple logic: if emissions are high, set the light to green
            if total_emissions > 5000:
                traffic_light_decision = 'green'
            else:
                traffic_light_decision = 'red'

            # Display the frame with bounding boxes (optional)
            annotated_frame = results[0].plot()  # Annotate frame with detections
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame = buffer.tobytes()

            # Yield the frame in byte format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

def calculate_emissions(vehicle_counts):
    total_emission = 0
    for vehicle, count in vehicle_counts.items():
        if vehicle in emission_mapping:
            total_emission += emission_mapping[vehicle] * count
    return total_emission

if __name__ == '__main__':
    app.run(debug=True)
