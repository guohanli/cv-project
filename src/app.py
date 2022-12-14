from flask import Flask

from api.densenet import densenet_api
from api.image_classifacation import image_classification_api
from api.vision_language import vision_language_api

app = Flask(__name__, static_url_path='', static_folder='../resource/album')
port = 5000

app.register_blueprint(densenet_api)
app.register_blueprint(image_classification_api)
app.register_blueprint(vision_language_api)

if __name__ == '__main__':
    app.run(port=port)
