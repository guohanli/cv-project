from flask import Blueprint
from flask import jsonify, request

image_classification_api = Blueprint('image_classification_api', __name__)


@image_classification_api.route('/get_covers')
def get_covers():
    return jsonify([{'img_path': 'http://127.0.0.1:5000/jack.png', 'category': 'people'},
                    {'img_path': 'http://127.0.0.1:5000/cat.png', 'category': 'animal'}])


@image_classification_api.route('/get_category_imgs')
def get_category_imgs():
    category = request.args.get("category")
    print(category)
    # todo 邱佳存，根据种类找到对应的图片数组
    return jsonify(
        [{'src': 'http://127.0.0.1:5000/jack.png', 'id': 'jack.png'},
         {'src': 'http://127.0.0.1:5000/cat.png', 'id': 'cat.png'},
         {'src': 'http://127.0.0.1:5000/dog.jpeg', 'id': 'dog.jpeg'},
         {'src': 'http://127.0.0.1:5000/jack.png', 'id': 'jack.png'},
         {'src': 'http://127.0.0.1:5000/cat.png', 'id': 'cat.png'},
         {'src': 'http://127.0.0.1:5000/dog.jpeg', 'id': 'dog.jpeg'}])
