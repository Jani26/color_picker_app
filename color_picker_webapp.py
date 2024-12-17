import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Label, Button, Canvas, PhotoImage
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

# Global variables
selected_colors = []
image = None
image_display = None

# Function to load the image
def load_image():
    global image, image_display
    file_path = filedialog.askopenfilename(title="Select an Image")
    if not file_path:
        print("No file selected!")
        return

    # Read and display the image
    image = cv2.imread(file_path)
    if image is None:
        print("Failed to load the image!")
        return
    
    # Convert to RGB and resize for display
    image_display = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_display, (500, 400))
    img = Image.fromarray(image_resized)
    img_tk = ImageTk.PhotoImage(img)

    # Update the canvas
    canvas.config(width=500, height=400)
    canvas.create_image(0, 0, anchor="nw", image=img_tk)
    canvas.image = img_tk  # Prevent garbage collection

    # Reset selected colors
    selected_colors.clear()
    status_label.config(text="Click on 3 points to select skin tone.")
    print("Image loaded. Start selecting points!")

# Function to handle mouse clicks on canvas
def pick_color(event):
    global selected_colors

    if image is None:
        return

    # Scale coordinates to original image size
    x_ratio = image.shape[1] / 500
    y_ratio = image.shape[0] / 400
    x, y = int(event.x * x_ratio), int(event.y * y_ratio)

    # Get RGB color at the clicked point
    r, g, b = image_display[y, x]
    selected_colors.append((r, g, b))

    # Update status and mark the point
    canvas.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, outline="red", width=2)
    print(f"Point {len(selected_colors)}: RGB = ({r}, {g}, {b})")

    # Calculate average after 3 points
    if len(selected_colors) == 3:
        calculate_average_color()

# Function to calculate the average color
def calculate_average_color():
    avg_r = np.mean([color[0] for color in selected_colors])
    avg_g = np.mean([color[1] for color in selected_colors])
    avg_b = np.mean([color[2] for color in selected_colors])

    avg_hex = "#{:02X}{:02X}{:02X}".format(int(avg_r), int(avg_g), int(avg_b))

    # Update the GUI with results
    status_label.config(text=f"Average Color: {avg_hex}")
    print(f"Average RGB: ({avg_r:.2f}, {avg_g:.2f}, {avg_b:.2f})")
    print(f"Average HEX: {avg_hex}")

    # Show color preview
    show_average_color(avg_r, avg_g, avg_b, avg_hex)

# Function to visualize the average color
def show_average_color(r, g, b, hex_code):
    fig, ax = plt.subplots(figsize=(2, 2))
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=(r/255, g/255, b/255)))
    ax.axis('off')
    plt.title(f"Average Skin Tone\n{hex_code}")
    plt.show()

# Initialize the GUI
root = tk.Tk()
root.title("Skin Tone Color Picker App")

# UI Elements
load_button = Button(root, text="Load Image", command=load_image, bg="lightblue", fg="black", width=15)
load_button.pack(pady=10)

status_label = Label(root, text="Upload an image and select points.", bg="white", fg="black")
status_label.pack()

canvas = Canvas(root, width=500, height=400, bg="gray")
canvas.pack()
canvas.bind("<Button-1>", pick_color)  # Left mouse button click to pick color

# Run the App
root.mainloop()

