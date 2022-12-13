from flask import Flask, jsonify

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


if __name__ == '__main__':
    app.run(port=port)
