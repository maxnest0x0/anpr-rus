import sys
sys.path.append('.')

from flask import Flask, request, jsonify, send_from_directory
import base64
import numpy as np
import cv2
from Detector.main import Detector

app = Flask(__name__, static_url_path='', static_folder='../web')

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return '', 400

        image_file = request.files['image']
        image_bytes = image_file.read()
        np_arr = np.frombuffer(image_bytes, np.uint8)
        cv2_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        detector = Detector(cv2_img)
        res_img, rects = detector.get_license_plate()

        img_buf = cv2.imencode('.png', res_img)[1]
        img_str = base64.b64encode(img_buf).decode('utf-8')
        img_str = f'data:image/png;base64,{img_str}'

        plates = []
        for x, y, w, h in rects:
            plates.append({
                'number': None,
                'accuracy': 0.5,
                'x': x.item(),
                'y': y.item(),
                'width': w.item(),
                'height': h.item(),
            })

        return jsonify({
            'image': img_str,
            'detected': len(rects),
            'recognized': 0,
            'plates': plates,
        })

    except Exception as e:
        print(f"Error during prediction: {e}")
        return '', 500

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)
