import cv2
import pytesseract
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import os

# Specify the path to the Tesseract executable (change this to your Tesseract installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Create a directory to store the detected faces
output_directory = "C:\BEIA\detect_faceA"
if not os.path.exists(output_directory):
    os.mkdir(output_directory)


def process_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = cv2.imread(file_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        text = pytesseract.image_to_string(binary_image)
        text_result.config(state='normal')
        text_result.delete(1.0, tk.END)
        text_result.insert(tk.END, text)
        text_result.config(state='disabled')

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Convert the image to grayscale for face detection
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Perform face detection
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.15, minNeighbors=5)

        for i, (x, y, w, h) in enumerate(faces):
            # Crop the detected face from the image
            face = image[y:y + h, x:x + w]

            # Save the detected face as an image file
            output_file = os.path.join(output_directory, f"face_{i + 1}.jpg")
            cv2.imwrite(output_file, face)

            # Display the detected face
            cv2.imshow("Detected Face", face)
            cv2.waitKey(0)


def clear_text():
    text_result.config(state='normal')
    text_result.delete(1.0, tk.END)
    text_result.config(state='disabled')


root = tk.Tk()
root.title("FlexiCross Project")

# Create a label for displaying the uploaded image
image_label = ttk.Label(root, text="Uploaded Image")
image_label.pack(pady=10)

# Create a button to select and process an image
process_button = ttk.Button(root, text="Select Image", command=process_image)
process_button.pack()

# Create a text widget for displaying extracted text
text_result = tk.Text(root, height=10, width=50)
text_result.pack(padx=10, pady=10)
text_result.config(state='disabled')

# Create a button to clear the extracted text
clear_button = ttk.Button(root, text="Clear Text", command=clear_text)
clear_button.pack()

# Keep the GUI event loop running
root.mainloop()
