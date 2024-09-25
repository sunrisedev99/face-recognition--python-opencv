import cv2
import face_recognition
import numpy as np
from datetime import datetime
from utils import save_faces, load_faces
import tkinter as tk
from tkinter import messagebox, simpledialog
from data import student_info_list  # Import the student info list

registered_faces = []  # Holds face encodings and associated names
load_faces()  # Load saved face data

def scan_face():
    global registered_faces
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open video device.")
        return

    messagebox.showinfo("Info", "Press 's' to scan and save the face.")
    
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            messagebox.showerror("Error", "Failed to capture frame from webcam.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow('Scan Face', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):  # Save face data when 's' is pressed
            if face_locations:
                try:
                    face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]

                    # Ask the user for student details (First name, last name, class, sex)
                    first_name = simpledialog.askstring("Input", "Enter the student's first name:")
                    last_name = simpledialog.askstring("Input", "Enter the student's last name:")
                    student_class = simpledialog.askstring("Input", "Enter the student's class (e.g., 1A, 1B, 2A):")

                    # Prompt the user for sex (Male or Female)
                    sex_options = ["Male", "Female"]
                    sex = simpledialog.askstring("Input", f"Enter the student's sex ({', '.join(sex_options)}):")

                    # Set the presence to "Absent" by default
                    presence_status = "Absent"

                    # Add student details to the student_info_list
                    student_info_list.append({
                        "first_name": first_name,
                        "last_name": last_name,
                        "class": student_class,
                        "sex": sex,  # Add the sex field
                        "time_of_scan": "N/A",  # Will be updated when they are recognized
                        "presence": presence_status
                    })

                    # Save the face encoding along with the student info
                    registered_faces.append((face_encoding, first_name + " " + last_name))
                    save_faces(registered_faces)

                    messagebox.showinfo("Info", f"Student {first_name} {last_name} registered with sex '{sex}' and status 'Absent'!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to encode face: {e}")
                break
        elif key == ord('q'):  # Quit scanning when 'q' is pressed
            break

    cap.release()
    cv2.destroyAllWindows()

# Continuous recognition to mark presence as "Present" when the student is recognized
def continuous_recognition():
    global registered_faces, student_info_list
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FPS, 30)  # Capture at a higher FPS
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open video device.")
        return

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)  # Downscale the frame for faster processing
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

        face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")  # Faster HOG-based model
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            # Compare the face encoding with registered faces
            for known_encoding, full_name in registered_faces:
                match = face_recognition.compare_faces([known_encoding], face_encoding, tolerance=0.5)
                if match[0]:
                    # Update the presence to "Present" in student_info_list
                    for student in student_info_list:
                        if full_name == student["first_name"] + " " + student["last_name"]:
                            student["presence"] = "Present"
                            student["time_of_scan"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            print(f"{full_name} marked as Present at {student['time_of_scan']}")

        # Display the video feed for debugging purposes
        cv2.imshow('Recognize Face', small_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()  # Release the camera resource
    cv2.destroyAllWindows()  # Close the video window
