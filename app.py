from flask import Flask, request, render_template, jsonify, send_file
import os
import uuid
from utils.triangulation import process_ab_measurements
from utils.ocr_reader import extract_ab_from_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['REPORT_FOLDER'] = 'reports'

# Ensure required folders exist
os.makedirs('uploads', exist_ok=True)
os.makedirs('reports', exist_ok=True)
os.makedirs('plots', exist_ok=True)

jobs = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    image = request.files['image']
    ab_length = float(request.form['ab_length'])

    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(filepath)

    ab_points = extract_ab_from_image(filepath)
    coords, report_path = process_ab_measurements(ab_points, ab_length, filename)

    jobs.append({
        'filename': filename,
        'ab_points': ab_points,
        'report': report_path
    })

    return send_file(report_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
