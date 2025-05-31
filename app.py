from flask import Flask, request, redirect, render_template_string
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home Route
@app.route("/")
def home():
    return "<h1>Pool Plotting App (PPO)</h1><p>Visit <a href='/upload'>/upload</a> to submit your A/B measurement sheet.</p>"

# Upload Page
@app.route("/upload", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        image = request.files.get("image")
        if not image:
            return "❌ No image uploaded."

        filename = secure_filename(image.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)

        # 👉 Insert OCR logic here in future (e.g. pytesseract)
        # Example:
        # from PIL import Image
        # import pytesseract
        # text = pytesseract.image_to_string(Image.open(filepath))

        return f"<h2>✅ Image uploaded successfully!</h2><p>Saved as: <code>{filename}</code></p>"

    # Render HTML form directly
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Upload A/B Measurement Sheet</title>
      <style>
        body { font-family: Arial, sans-serif; background: #f4f4f4; padding: 40px; }
        h1 { text-align: center; color: #222; }
        form {
          background: white;
          padding: 20px;
          max-width: 500px;
          margin: auto;
          border-radius: 10px;
          box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        input[type="file"] {
          width: 100%;
          padding: 10px;
          margin: 10px 0 20px 0;
          border: 1px solid #ccc;
          border-radius: 5px;
        }
        button {
          background-color: #007bff;
          color: white;
          border: none;
          padding: 10px 20px;
          border-radius: 5px;
          cursor: pointer;
        }
        button:hover {
          background-color: #0056b3;
        }
        .note {
          font-size: 0.9em;
          color: #555;
          margin-bottom: 20px;
        }
      </style>
    </head>
    <body>
      <h1>Upload A/B Measurement Sheet</h1>
      <form action="/upload" method="POST" enctype="multipart/form-data">
        <label for="image">Select your photo (JPG/PNG):</label><br>
        <input type="file" name="image" accept="image/*" required><br>
        <div class="note">We’ll use OCR to read your measurements automatically.</div>
        <button type="submit">Upload & Process</button>
      </form>
    </body>
    </html>
    """)

# Run App
if __name__ == "__main__":
    app.run(debug=True)
