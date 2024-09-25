import json
import numpy as np
from tkinter import messagebox

def save_faces(registered_faces):
    face_data = [
        {"name": name, "encoding": encoding.tolist()}
        for encoding, name in registered_faces
    ]
    with open("registered_faces.json", "w") as f:
        json.dump(face_data, f)
    print("Faces saved to registered_faces.json")

def load_faces():
    global registered_faces
    try:
        with open("registered_faces.json", "r") as f:
            face_data = json.load(f)
        registered_faces = [(np.array(item["encoding"]), item["name"]) for item in face_data]
        print("Faces loaded from registered_faces.json")
    except FileNotFoundError:
        print("No previous face data found.")
