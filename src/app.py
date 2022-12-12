from flask import Flask, jsonify

from api.densenet import densenet_api

app = Flask(__name__)

app.register_blueprint(densenet_api)


@app.route('/')
def predict():
    return jsonify({'msg': 'HELLO', 'class_name': 'Cat'})


if __name__ == '__main__':
    app.run()
