from flask import Flask, request, jsonify, send_from_directory
import os
from flask_cors import CORS
import cv2
from run import correct_color

app = Flask(__name__)

CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://192.168.1.4:3000"])

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['STATIC_FOLDER'] = 'static'

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

        severity_map = {
            'Mild': 0.25,
            'Moderate': 0.5,
            'Severe': 0.75
        }
        
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

def extract_frames_from_video(input_path):
    cap = cv2.VideoCapture(input_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        yield frame
    cap.release()

def save_frame(frame, frame_count):
    frame_filename = f"frame_{frame_count}.jpg"
    frame_path = os.path.join(app.config['UPLOAD_FOLDER'], frame_filename)
    cv2.imwrite(frame_path, frame)
    return frame_path

def save_video_from_frames(frames, output_path, width, height, fps=30):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # codec for .mp4 files
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame in frames:
        out.write(frame)

    out.release()

def process_video(input_path, processed_media_path, blindness_type, severity):
    frame_count = 0
    processed_frames = []

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Video not found: {input_path}")

    for frame in extract_frames_from_video(input_path):
        frame_count += 1
        
        frame_path = save_frame(frame, frame_count)

        if frame_path is None:
            continue
        
        try:
            processed_frame = correct_color(frame_path, blindness_type, severity)
            processed_frames.append(processed_frame)
        except Exception as e:
            continue

    # Save the processed video
    if processed_frames:
        first_frame = processed_frames[0]
        height, width, _ = first_frame.shape
        save_video_from_frames(processed_frames, processed_media_path, width, height)

    return True, frame_count

@app.route('/static/uploads/<filename>')
def serve_uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/static/processed/<filename>')
def serve_processed_file(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
