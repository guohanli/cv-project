import json
import os
import time

from flask import Blueprint
from flask import jsonify, request

from utils import album_path

image_classification_api = Blueprint('image_classification_api', __name__)


@image_classification_api.route('/new_image', methods=['POST'])
def new_image():
    file = request.files.get('new_image')
    file_name = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + '.jpeg'
    file_save_path = os.path.join(album_path, file_name)
    file.save(file_save_path)
    return ''

@image_classification_api.route('/delete_image', methods=['POST'])
def delete_image():
    file_name = json.loads(request.data)
    pass
    return ''


@image_classification_api.route('/get_covers')
def get_covers():
    return jsonify([{'img_path': 'http://127.0.0.1:5000/jack.png', 'category': 'people'},
                    {'img_path': 'http://127.0.0.1:5000/cat.png', 'category': 'animal'}])


@image_classification_api.route('/get_category_imgs')
def get_category_imgs():
    category = request.args.get("category")
    # todo 邱佳存，根据种类找到对应的图片数组
    return jsonify(
        [{'src': 'http://127.0.0.1:5000/jack.png', 'id': 'jack.png'},
         {'src': 'http://127.0.0.1:5000/cat.png', 'id': 'cat.png'},
         {'src': 'http://127.0.0.1:5000/dog.jpeg', 'id': 'dog.jpeg'},
         {'src': 'http://127.0.0.1:5000/jack.png', 'id': 'jack.png'},
         {'src': 'http://127.0.0.1:5000/cat.png', 'id': 'cat.png'},
         {'src': 'http://127.0.0.1:5000/dog.jpeg', 'id': 'dog.jpeg'}])
