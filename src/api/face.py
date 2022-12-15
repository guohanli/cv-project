from flask import Blueprint
from flask import jsonify, request

from utils import img_url2path, img_path2name, img_path2url, img_name2path

face_api = Blueprint('face_api', __name__)


@face_api.route('/get_face_covers')
def get_face_covers():
    # todo 王婧馨
    return jsonify([{'src': 'http://127.0.0.1:5000/jack.png', 'face_category_id': '1', 'count': '3'},
                    {'src': 'http://127.0.0.1:5000/cat.png', 'face_category_id': '2', 'count': '5'}])


@face_api.route('/get_somebody_faces')
def get_somebody_faces():
    # todo 王婧馨
    face_category_id = request.args.get('face_category_id')
    return jsonify(
        [{'src': 'http://127.0.0.1:5000/jack.png', 'id': 'jack.png'},
         {'src': 'http://127.0.0.1:5000/cat.png', 'id': 'cat.png'},
         {'src': 'http://127.0.0.1:5000/dog.jpeg', 'id': 'dog.jpeg'},
         {'src': 'http://127.0.0.1:5000/jack.png', 'id': 'jack.png'},
         {'src': 'http://127.0.0.1:5000/cat.png', 'id': 'cat.png'},
         {'src': 'http://127.0.0.1:5000/dog.jpeg', 'id': 'dog.jpeg'}])


@face_api.route('/get_animate')
def get_animate():
    img_url = request.args.get("img_url")
    img_path = img_url2path(img_url)
    img_name = img_path2name(img_path)
    # todo 王婧馨，获取生成的动画图片的路径
    img_animate_path = '/Users/lgh/PycharmProjects/cv-project/resource/album/dog.jpeg'
    img_animate_name = img_name2path(img_animate_path)
    img_animate_url = img_path2url(img_animate_path)
    return jsonify({'src': img_animate_url, 'id': img_animate_name})
