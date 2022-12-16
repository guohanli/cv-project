from flask import Blueprint
from flask import jsonify, request

import os
from PIL import Image
from utils import transform_image_bytes2tensor, img_path2url
from model.retrieval_model import image_retrieval, getMaxSimilarity

image_retrieval_api = Blueprint('image_retrieval_api', __name__)

@image_retrieval_api.route('/search_img_by_img', methods=['POST'])
def search_img_by_img():
    file = request.files.get('query_image')
    img_bytes = file.read()
    img = transform_image_bytes2tensor(img_bytes)
    
    # todo 刘雯，根据图片找到最佳匹配图片
    img_path = 'C:/Users/mi/cv-project/resource/images'
    query_path = 'C:/Users/mi/cv-project/resource/images/query/'
    scores = image_retrieval(base_path=img_path, query_path=query_path, base_batch_size=10)
    img_name, max_score = getMaxSimilarity(scores)
    img_item_path = os.path.join(img_path, img_name)
    img = Image.Open(img_item_path)
    img.show()

    img_url = img_path2url(img_item_path)
    # return jsonify('http://127.0.0.1:5000/dog.jpeg')
    return img_url
