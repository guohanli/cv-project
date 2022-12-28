import time

from flask import Blueprint
from flask import jsonify, request

import os
from PIL import Image

import sys
sys.path.append("..")

import utils
# from utils import transform_image_bytes2tensor, img_path2url
from model.image_retrieval.retrieval_model import image_retrieval, getMaxSimilarity

image_retrieval_api = Blueprint('image_retrieval_api', __name__)

@image_retrieval_api.route('/search_img_by_img', methods=['POST'])
def search_img_by_img():

    file = request.files.get('query_image')
    img_bytes = file.read()
    img = utils.transform_image_bytes2tensor(img_bytes)
    
    # todo 刘雯，根据图片找到最佳匹配图片

    # img_path, only the folder of images
    img_path = 'resource/album'
    # query_path, path to the query image
    query_path = 'resource/album/cat.png' 
    query_name = 'cat.png'
    
    scores = image_retrieval(base_path=img_path, query_path=query_path, base_batch_size=28)
    
    img_name, max_score = getMaxSimilarity(scores, query_name)
    img_item_path = os.path.join(img_path, img_name)
    img = Image.open(img_item_path)
    img.show()

    img_url = utils.img_path2url(img_item_path)
    return jsonify(img_url)
