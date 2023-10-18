import os
import dlib
import face_recognition
from PIL import Image
import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
email_sender = 'your_mail'  # Your email address
email_receiver = 'receiver_email@example.com'  # Receiver's email address
email_password = '......'  # Your email password
smtp_server = 'smtp.gmail.com'  # SMTP server (for Gmail)

# Directory containing known faces
known_faces_dir = "C:\\BEIA\\datasets"

# Load the reference dataset (known faces)
known_faces = []
known_face_names = []

for filename in os.listdir(known_faces_dir):
    if filename.endswith(".jpg"):
        # Load the image
        known_image = face_recognition.load_image_file(os.path.join(known_faces_dir, filename))

        # Encode the face
        known_face_encoding = face_recognition.face_encodings(known_image)[0]

        # Extract the name (remove the file extension)
        person_name = os.path.splitext(filename)[0]

        # Append the encoding and name to the lists
        known_faces.append(known_face_encoding)
        known_face_names.append(person_name)

# Initialize the face detector from dlib
face_detector = dlib.get_frontal_face_detector()

# Function to send an alert email
def send_email_alert(matched_name):
    subject = "Face Recognition Alert"
    body = f"Face recognized as {matched_name}"

    message = MIMEMultipart()
    message['From'] = email_sender
    message['To'] = email_receiver
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, 587)
        server.starttls()
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_receiver, message.as_string())
        server.quit()
    except Exception as e:
        messagebox.showerror("Email Error", str(e))

# Function to handle image upload
def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        input_image = face_recognition.load_image_file(file_path)
        input_face_locations = face_recognition.face_locations(input_image)
        input_face_encodings = face_recognition.face_encodings(input_image, input_face_locations)

        if len(input_face_encodings) == 0:
            messagebox.showerror("no", "No face found in the selected image.")
            return

        for (top, right, bottom, left) in input_face_locations:
            # Compare the input face to known faces
            face_encoding = face_recognition.face_encodings(input_image, [(top, right, bottom, left)])[0]
            matches = face_recognition.compare_faces(known_faces, face_encoding)

            if True in matches:
                # Find the name of the known face that matches
                name = known_face_names[matches.index(True)]
                result_label.config(text=f"Face in the input image matches {name}.")
#                send_email_alert(name)
                messagebox.showinfo("Alert", f"Face recognized as {name}.\nAlert email sent.")
            else:
                result_label.config(text="Face in the input image does not match any known face.")

        # Draw rectangles around the detected faces
        input_image_with_rectangles = input_image.copy()
        for (top, right, bottom, left) in input_face_locations:
            cv2.rectangle(input_image_with_rectangles, (left, top), (right, bottom), (0, 0, 255), 2)

        # Save the modified image as 'temp_image.jpg'
        Image.fromarray(input_image_with_rectangles).save('temp_image.jpg')

# Create the main window
root = tk.Tk()

root.geometry("600x150")
root.title("Face Recognition App")

# Create a button to upload an image
upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack(pady=10)

# Create a label to display the result
result_label = tk.Label(root, text="", font=("Helvetica", 14))
result_label.pack()

# Start the Tkinter main loop
root.mainloop()
