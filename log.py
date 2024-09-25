# log.py
import csv
import tkinter as tk
from tkinter import Toplevel, Text, Scrollbar, messagebox
from datetime import datetime
from data import student_info_list  # Import from data.py

# Function to export the student info list to a CSV file
def export_student_info_to_csv():
    filename = f"student_info_{datetime.now().strftime('%Y%m%d')}.csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        # Write the header row with student information fields
        writer.writerow(["First Name", "Last Name", "Class", "Sex", "Time of Scan", "Presence"])
        # Write the student information from the list
        for student in student_info_list:
            writer.writerow([student['first_name'], student['last_name'], student['class'], student['sex'], student['time_of_scan'], student['presence']])

    messagebox.showinfo("Info", f"Student information saved as {filename}")

# Function to view the student info list in the GUI
def view_student_info_list():
    if not student_info_list:
        messagebox.showinfo("Info", "No student information available.")
        return

    # Create a new window to display the student information list
    info_window = Toplevel()
    info_window.title("Student Information List")

    text_area = Text(info_window, height=20, width=80)
    scrollbar = Scrollbar(info_window, command=text_area.yview)
    text_area.configure(yscrollcommand=scrollbar.set)

    # Insert the student information list into the text area
    text_area.insert(tk.END, "First Name\tLast Name\tClass\tSex\tTime of Scan\tPresence\n")
    text_area.insert(tk.END, "-" * 80 + "\n")
    for student in student_info_list:
        text_area.insert(tk.END, f"{student['first_name']}\t{student['last_name']}\t{student['class']}\t{student['sex']}\t{student['time_of_scan']}\t{student['presence']}\n")

    text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_area.config(state=tk.DISABLED)

# Function to clear the presence and time of scan for all students
def clear_presence_list():
    # Confirm if the user really wants to clear the list
    confirm = messagebox.askyesno("Confirmation", "Are you sure you want to reset the presence and time of scan for all students?")
    
    if confirm:  # If the user clicks "Yes"
        for student in student_info_list:
            student['presence'] = "Absent"  # Reset presence to "Absent"
            student['time_of_scan'] = "N/A"  # Reset time of scan to "N/A"
        
        messagebox.showinfo("Info", "All student presence and time of scan have been reset.")
