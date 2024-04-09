from flask import current_app, request, jsonify
from werkzeug.utils import secure_filename
import os

from .tasks import process_video

def register_routes(app):
    @app.route('/upload', methods=['POST'])
    def upload_video():
        if 'video' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['video']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

            process_video.delay(filename)

            return jsonify({'message': 'File uploaded successfully, processing will start shortly.', 'filename': filename}), 200
        else:
            return jsonify({'error': 'Invalid file type'}), 400

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp4', 'avi', 'mov'}
