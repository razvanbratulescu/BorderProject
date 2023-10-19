import dlib
import face_recognition
from PIL import Image
import cv2
import io
from IPython.display import display

# Load the reference dataset (known faces)
known_faces = []

# Load images of known faces and encode them
known_image_1 = face_recognition.load_image_file("face_2.jpg")
known_face_encoding_1 = face_recognition.face_encodings(known_image_1)[0]
known_faces.append(known_face_encoding_1)

# Load the input image you want to compare
input_image = face_recognition.load_image_file("1.jpg")
input_face_locations = face_recognition.face_locations(input_image)
input_face_encodings = face_recognition.face_encodings(input_image, input_face_locations)

# Initialize the face detector from dlib
face_detector = dlib.get_frontal_face_detector()

for (top, right, bottom, left) in input_face_locations:
    # Compare the input face to known faces
    face_encoding = face_recognition.face_encodings(input_image, [(top, right, bottom, left)])[0]
    matches = face_recognition.compare_faces(known_faces, face_encoding)

    if True in matches:
        print("Face in the input image matches a known face.")
    else:
        print("Face in the input image does not match any known face.")

# Draw rectangles around the detected faces
input_image_with_rectangles = input_image.copy()
for (top, right, bottom, left) in input_face_locations:
    cv2.rectangle(input_image_with_rectangles, (left, top), (right, bottom), (0, 0, 255), 2)

# Display the image using PIL (Pillow)
display(Image.fromarray(input_image_with_rectangles))