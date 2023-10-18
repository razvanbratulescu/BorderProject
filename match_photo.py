import os
import dlib
import face_recognition
from PIL import Image
import cv2
import tkinter as tk

# Directory containing known faces
known_faces_dir = "C:\...\datasets"

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

# Load the input image you want to compare
input_image = face_recognition.load_image_file(r"C:\...\1.JPEG")
input_face_locations = face_recognition.face_locations(input_image)
input_face_encodings = face_recognition.face_encodings(input_image, input_face_locations)

# Initialize the face detector from dlib
face_detector = dlib.get_frontal_face_detector()

for (top, right, bottom, left) in input_face_locations:
    # Compare the input face to known faces
    face_encoding = face_recognition.face_encodings(input_image, [(top, right, bottom, left)])[0]
    matches = face_recognition.compare_faces(known_faces, face_encoding)

    if True in matches:
        # Find the name of the known face that matches
        name = known_face_names[matches.index(True)]
        print(f"Face in the input image matches {name}.")
    else:
        print("Face in the input image does not match any known face.")

# Draw rectangles around the detected faces
input_image_with_rectangles = input_image.copy()
for (top, right, bottom, left) in input_face_locations:
    cv2.rectangle(input_image_with_rectangles, (left, top), (right, bottom), (0, 0, 255), 2)

# Save the modified image as 'temp_image.jpg'
Image.fromarray(input_image_with_rectangles).save('temp_image.jpg')

# Display the image using Tkinter
root = tk.Tk()
root.title("Input Image with Face Detection")

# Load and display the image with Tkinter
image = Image.open('temp_image.jpg')
photo = tk.PhotoImage(image=image)
label = tk.Label(root, image=photo)
label.pack()

root.mainloop()
