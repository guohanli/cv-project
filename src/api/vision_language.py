import json

from flask import Blueprint
from flask import jsonify, request

vision_language_api = Blueprint('vision_language_api', __name__)


@vision_language_api.route('/search_img_by_text', methods=['POST'])
def search_img_by_text():
    search_text = json.loads(request.data)
    # todo 胡金景，根据文本找到最佳匹配图片
    return jsonify('http://127.0.0.1:5000/dog.jpeg')
