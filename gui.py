# gui.py
import tkinter as tk
from camera import scan_face, continuous_recognition
from log import view_student_info_list, export_student_info_to_csv, clear_presence_list  # Make sure this import is correct

def setup_gui():
    window = tk.Tk()  # Initialize the Tkinter window
    window.title("Face Recognition System")  # Set the title of the window

    # Add a label for the header
    label = tk.Label(window, text="Face Recognition System", font=("Helvetica", 16))
    label.pack(pady=20)  # Add some vertical padding

    # Button to scan a new face
    scan_button = tk.Button(window, text="Scan Face", command=scan_face, font=("Helvetica", 14))
    scan_button.pack(pady=10)  # Add some vertical padding

    # Button to start continuous recognition
    recognize_button = tk.Button(window, text="Start Continuous Recognition", command=continuous_recognition, font=("Helvetica", 14))
    recognize_button.pack(pady=10)  # Add some vertical padding

    # Button to view the student info list
    info_button = tk.Button(window, text="View Student Info List", command=view_student_info_list, font=("Helvetica", 14))
    info_button.pack(pady=10)  # Add some vertical padding

    # Button to export the student info list to CSV
    export_info_button = tk.Button(window, text="Export Student Info to CSV", command=export_student_info_to_csv, font=("Helvetica", 14))
    export_info_button.pack(pady=10)  # Add some vertical padding

    # Button to clear the presence and time of scan for all students
    clear_presence_button = tk.Button(window, text="Clear Presence List", command=clear_presence_list, font=("Helvetica", 14))
    clear_presence_button.pack(pady=10)  # Add some vertical padding

    # Exit button to close the application
    exit_button = tk.Button(window, text="Exit", command=window.quit, font=("Helvetica", 14))
    exit_button.pack(pady=10)  # Add some vertical padding

    # Set the window geometry to ensure it’s large enough to display all the buttons
    window.geometry("300x500")  # Adjust the window size

    window.mainloop()  # Start the GUI main loop
