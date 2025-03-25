from flask import Flask, Response, request, jsonify, send_file, send_from_directory
import os
import cv2
import numpy as np
from flask_cors import CORS
from run import correct_color  # Ensure this function correctly processes images & frames.

app = Flask(__name__)

CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://192.168.1.4:3000"])

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def allowed_file(filename, file_type):
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in (ALLOWED_IMAGE_EXTENSIONS if file_type == 'image' else ALLOWED_VIDEO_EXTENSIONS)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = None
    file_type = None

    if 'image' in request.files:
        file = request.files['image']
        file_type = 'image'
    elif 'video' in request.files:
        file = request.files['video']
        file_type = 'video'
    else:
        return jsonify({"error": "No file part"}), 400

    if file and allowed_file(file.filename, file_type):
        filename = file.filename
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)

        blindness_type = request.form.get('colorBlindnessType')
        severity_str = request.form.get('severity')

        severity_map = {'Mild': 0.25, 'Moderate': 0.5, 'Severe': 0.75}
        severity = severity_map.get(severity_str, 0.25)

        processed_media_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)

        if file_type == 'image':
            correct_color(save_path, blindness_type, severity, processed_media_path)
            return jsonify({"correctedMediaURL": f"http://{request.host}/static/processed/{filename}"})

        elif file_type == 'video':
            success, frame_count = process_video(save_path, processed_media_path, blindness_type, severity)
            if success:
                return jsonify({
                    "correctedMediaURL": f"http://{request.host}/static/processed/{filename}",
                    "framesProcessed": frame_count
                })
            else:
                return jsonify({"error": "Failed to process video"}), 500

    return jsonify({"error": "Invalid file format"}), 400

def process_video(input_path, output_path, blindness_type, severity):
    frame_count = 0

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        return False, 0

    fps = cap.get(cv2.CAP_PROP_FPS)
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        try:
            if isinstance(frame, np.ndarray):
                corrected_frame = correct_color(None, blindness_type, severity, frame=frame)
                corrected_frame = cv2.resize(corrected_frame, (width, height))
                out.write(corrected_frame)
            else:
                print(f"Skipping frame {frame_count}: Invalid frame type {type(frame)}")
        except Exception as e:
            print(f"Error processing frame {frame_count}: {e}")
            continue

    cap.release()
    out.release()
    return True, frame_count

@app.route('/static/processed/<filename>')
def serve_processed_file(filename):
    file_path = os.path.join(PROCESSED_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    return send_file(file_path, as_attachment=False, mimetype="video/mp4")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
