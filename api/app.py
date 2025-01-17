from flask import Flask, request, jsonify, send_from_directory
import base64
import numpy as np
import cv2
from Detector.main import Detector

app = Flask(__name__, static_url_path='', static_folder='../web')

@app.route('/api/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return 'image is required', 400

    img_buf = request.files['image'].read()
    np_arr = np.frombuffer(img_buf, np.uint8)
    cv2_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    detector = Detector(cv2_img)
    result = detector.get_license_plate()

    img_buf = cv2.imencode('.png', detector.img)[1]
    img_str = base64.b64encode(img_buf).decode('utf-8')
    img_str = f'data:image/png;base64,{img_str}'

    plates = []
    for plate_img, plate_text, confidence, (x, y), (w, h) in result:
        plate_img_buf = cv2.imencode('.png', plate_img)[1]
        plate_img_str = base64.b64encode(plate_img_buf).decode('utf-8')
        plate_img_str = f'data:image/png;base64,{plate_img_str}'

        plates.append({
            'image': plate_img_str,
            'number': plate_text,
            'accuracy': confidence,
            'x': x,
            'y': y,
            'width': w,
            'height': h,
        })

    return jsonify({
        'image': img_str,
        'detected': detector.detected,
        'recognized': detector.recognized,
        'plates': plates,
    })

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

def run_api():
    app.run('0.0.0.0')
