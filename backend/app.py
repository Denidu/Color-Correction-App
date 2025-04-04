from flask import Flask, Response, request, jsonify, send_file, send_from_directory
import os
import cv2
import numpy as np
from flask_cors import CORS
from run import correct_color  

app = Flask(__name__)

CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://192.168.1.4:3000"])

UPLOAD_FOLDER_NAME = 'uploads'
PROCESSED_FOLDER_NAME = 'processed'
ALLOWED_IMAGE_EXTENSIONS_AS = {'png', 'jpg', 'jpeg'}
ALLOWED_VIDEO_EXTENSIONS_AS = {'mp4', 'mov'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_NAME
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER_NAME

os.makedirs(UPLOAD_FOLDER_NAME, exist_ok=True)
os.makedirs(PROCESSED_FOLDER_NAME, exist_ok=True)

def allow_files(filename, file_type):
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in (ALLOWED_IMAGE_EXTENSIONS_AS if file_type == 'image' else ALLOWED_VIDEO_EXTENSIONS_AS)

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

    if file and allow_files(file.filename, file_type):
        filename = file.filename
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)

        color_blindness_type = request.form.get('colorBlindnessType')
        severity = request.form.get('severity')

        severity_level = {'Mild': 0.25, 'Moderate': 0.5, 'Severe': 0.75}
        severity = severity_level.get(severity, 0.25)

        processed_media_location = os.path.join(app.config['PROCESSED_FOLDER'], filename)

        if file_type == 'image':
            correct_color(save_path, color_blindness_type, severity, processed_media_location)
            return jsonify({"correctedMediaURL": f"http://{request.host}/static/processed/{filename}"})

        elif file_type == 'video':
            success, frame_count = process_video_correction(save_path, processed_media_location, color_blindness_type, severity)
            if success:
                return jsonify({
                    "correctedMediaURL": f"http://{request.host}/static/processed/{filename}",
                    "framesProcessed": frame_count
                })
            else:
                return jsonify({"error": "Failed to process video"}), 500

    return jsonify({"error": "Invalid file format"}), 400

def process_video_correction(input_path, output_path, blindness_type, severity):
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
    file_path = os.path.join(PROCESSED_FOLDER_NAME, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    return send_file(file_path, as_attachment=False, mimetype="video/mp4")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
