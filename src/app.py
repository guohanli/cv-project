import json

from flask import Flask, jsonify, request

from api.densenet import densenet_api

app = Flask(__name__, static_url_path='', static_folder='../resource/album')
port = 5000

app.register_blueprint(densenet_api)


@app.route('/')
def predict():
    return jsonify({'msg': 'HELLO', 'class_name': 'Cat'})


@app.route('/get_covers')
def get_covers():
    return jsonify([{'img_path': 'http://127.0.0.1:5000/jack.png', 'category': 'people'},
                    {'img_path': 'http://127.0.0.1:5000/cat.png', 'category': 'animal'}])


@app.route('/get_category_imgs')
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


@app.route('/search_img_by_text', methods=['POST'])
def search_img_by_text():
    search_text = json.loads(request.data)
    # todo 胡金景，根据文本找到最佳匹配图片
    return jsonify('http://127.0.0.1:5000/dog.jpeg')


if __name__ == '__main__':
    app.run(port=port)
