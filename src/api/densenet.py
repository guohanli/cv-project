from flask import Blueprint
from flask import jsonify, request

from model.densenet.load_model import get_prediction

densenet_api = Blueprint('densenet_api', __name__)


@densenet_api.route('/densenet/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        class_id, class_name = get_prediction(image_bytes=img_bytes)
        return jsonify({'class_id': class_id, 'class_name': class_name})