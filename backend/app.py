from flask import Flask, request, jsonify, send_from_directory
import os
from flask_cors import CORS  # Make sure this is imported
from run import correct_color

app = Flask(__name__)

# Allow access from your Flutter app URL
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://192.168.1.4:3000"])

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Ensure folders exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

def allowed_file(filename, file_type):
    """Check if file type is allowed (image or video)."""
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in (ALLOWED_IMAGE_EXTENSIONS if file_type == 'image' else ALLOWED_VIDEO_EXTENSIONS)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' in request.files:
        file = request.files['image']
        file_type = 'image'
    else:
        return jsonify({"error": "No file part"}), 400

    if file and allowed_file(file.filename, file_type):
        filename = file.filename
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)

        # Get color blindness type and severity
        blindness_type = request.form.get('colorBlindnessType')
        severity = float(request.form.get('severity'))

        # Process image for color correction
        processed_image_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)

        # Call the function from `run.py` to apply color correction
        correct_color(save_path, blindness_type, severity, processed_image_path)

        # Return the URL of the corrected image
        return jsonify({"correctedMediaURL": f"http://{request.host}/static/processed/{filename}"})

    return jsonify({"error": "Invalid file format"}), 400


@app.route('/static/uploads/<filename>')
def serve_uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/static/processed/<filename>')
def serve_processed_file(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
