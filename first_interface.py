import tkinter as tk
import subprocess

def open_bulletin_window():
    subprocess.Popen(["python", "id_card_textwithocr.py"], shell=True)

def open_passport_window():
    subprocess.Popen(["python", "textwithocr.py"], shell=True)

# Create the main window
root = tk.Tk()
root.geometry("300x150")
root.title("FlexiCross Project")

# Create buttons for "passport" and "bulletin"
passport_button = tk.Button(root, text="Passport", command=open_passport_window)
passport_button.pack(pady=20)

bulletin_button = tk.Button(root, text="Id_Card", command=open_bulletin_window)
bulletin_button.pack(pady=20)

root.mainloop()