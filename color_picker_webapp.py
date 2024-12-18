import os
import cv2
import numpy as np
from sklearn.cluster import KMeans
from flask import Flask, request, render_template, redirect, url_for
import matplotlib.pyplot as plt

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Functions for Dominant Color and Skin Tone Classification
def get_dominant_color(image_path, k=1):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError("Image not found. Check the file path.")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((-1, 3))
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(image)
    dominant_color = kmeans.cluster_centers_.astype(int)[0]
    return tuple(dominant_color)

def classify_skin_tone(rgb):
    skin_tone_ranges = {
        "Very Fair": (255, 223, 196),
        "Fair": (240, 213, 182),
        "Light Beige": (232, 199, 185),
        "Medium Beige": (209, 178, 149),
        "Tan": (184, 142, 111),
        "Caramel": (167, 111, 90),
        "Bronze": (141, 74, 67),
        "Deep Brown": (106, 62, 46),
        "Very Dark Brown": (75, 45, 26),
    }
    min_distance = float('inf')
    closest_tone = None
    for tone, value in skin_tone_ranges.items():
        distance = np.linalg.norm(np.array(rgb) - np.array(value))
        if distance < min_distance:
            min_distance = distance
            closest_tone = tone
    return closest_tone

# Refined Palettes (add your palettes here as you did previously)
refined_palettes = { ... }  # Paste your refined_palettes dictionary here
descriptions = { ... }  # Paste descriptions here

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle file upload
        file = request.files["file"]
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            # Process the image
            dominant_rgb = get_dominant_color(filepath)
            skin_tone = classify_skin_tone(dominant_rgb)
            palettes = refined_palettes.get(skin_tone, {})
            
            return render_template("index.html", 
                                   dominant_rgb=dominant_rgb, 
                                   skin_tone=skin_tone, 
                                   palettes=palettes,
                                   descriptions=descriptions,
                                   image_path=filepath)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
