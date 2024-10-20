from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import cv2
from threading import Thread
from queue import Queue
from ultralytics import YOLO
from wtforms.validators import DataRequired
from flask import request
import os
from ultralytics import YOLO
from flask import render_template, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define YOLO model
try:
    model = YOLO("best.pt")
except Exception as e:
    print(f"Error loading YOLO model: {e}")

class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

users = [
    User(1, 'user@example.com', 'password')
]

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

@login_manager.user_loader
def load_user(user_id):
    return next((user for user in users if user.id == int(user_id)), None)

class WebcamForm(FlaskForm):
    start_webcam = SubmitField('Start Webcam')
    stop_webcam = SubmitField('Stop Webcam')

# Function to process webcam frames with YOLO
def process_frames(queue):
    try:
        while True:
            frame = queue.get()
            if frame is None:
                break

            # Process the frame with YOLO model
            results = model(frame)
            annotated_frame = results[0].plot()

            # Send the annotated frame to the main thread for display
            queue.put(annotated_frame)
    except Exception as e:
        print(f"Error in process_frames: {e}")

# Index route
@app.route('/')
def index():
    return render_template('index.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = next((u for u in users if u.email == email and u.password == password), None)

        if user:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if any(u.email == email for u in users):
            flash('Email is already registered. Please log in.', 'danger')
            return redirect(url_for('login'))

        new_user = User(len(users) + 1, email, password)
        users.append(new_user)

        login_user(new_user)
        flash('Account created successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

# Webcam route
@app.route('/webcam', methods=['GET', 'POST'])
@login_required
def webcam():
    form = WebcamForm()

    # Queue to communicate between threads
    queue = Queue()

    # Thread to process frames with YOLO
    yolo_thread = Thread(target=process_frames, args=(queue,), daemon=True)
    yolo_thread.start()

    # Video capture object
    cap = cv2.VideoCapture(0)

    try:
        while True:
            success, frame = cap.read()

            if success:
                # Send the frame to the YOLO processing thread
                queue.put(frame)

                # Receive annotated frame from YOLO processing thread
                annotated_frame = queue.get()

                # Display the annotated frame
                cv2.imshow("YOLOv8 Interface", annotated_frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    except Exception as e:
        print(f"Error in webcam route: {e}")
    finally:
        # Release resources
        cap.release()
        queue.put(None)  # Signal YOLO processing thread to exit
        yolo_thread.join()
        cv2.destroyAllWindows()

    return render_template('webcam.html', form=form)

# New route for handling image uploads
@app.route('/upload_image', methods=['POST'])
@login_required
def upload_image():
    if 'image' in request.files:
        image = request.files['image']

        # Save the uploaded image to a folder (adjust the path as needed)
        image_path = os.path.join('static', 'uploads', image.filename)
        image.save(image_path)

        # Perform object detection on the uploaded image using the YOLO model
        yolo_model = YOLO("best3.pt")
        results = yolo_model.predict(image_path, show=True, conf=0.3)

        # Extract and print the labels for the detected signs
        detected_labels = get_detected_labels(results) if results else []
        print("Detected Labels:", detected_labels)

        return "Detection results printed in the terminal."

    else:
        flash('No image file provided.', 'danger')
        return redirect(url_for('index'))

def get_detected_labels(results):
    try:
        # Check if 'names' attribute is present in the results
        if hasattr(results, 'names'):
            return [results.names[pred[6].int()] for pred in results[0]]
        else:
            # Handle the case where 'names' attribute is not present
            return []
    except (AttributeError, IndexError, TypeError):
        return []


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
