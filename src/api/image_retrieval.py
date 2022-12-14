from flask import Blueprint
from flask import jsonify, request

from utils import transform_image_bytes2tensor

image_retrieval_api = Blueprint('image_retrieval_api', __name__)


@image_retrieval_api.route('/search_img_by_img', methods=['POST'])
def search_img_by_img():
    file = request.files.get('query_image')
    img_bytes = file.read()
    img = transform_image_bytes2tensor(img_bytes)
    # todo 刘雯，根据图片找到最佳匹配图片
    return jsonify('http://127.0.0.1:5000/dog.jpeg')
