import json

from flask import Blueprint
from flask import jsonify, request

import torch
import clip
from PIL import Image
import os
from utils import img_path2url

def match(str1,sent):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    image = preprocess(Image.open(str1)).unsqueeze(0).to(device)
    text = clip.tokenize([sent]).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)
        logits_per_image, logits_per_text = model(image, text)
        similarity = str(logits_per_image)[9:13]
        res = float(similarity)
        return res

vision_language_api = Blueprint('vision_language_api', __name__)


@vision_language_api.route('/search_img_by_text', methods=['POST'])
def search_img_by_text():
    sent = json.loads(request.data)
    current_path = os.path.dirname(__file__)
    path0 = os.path.join(current_path, '..', 'resource', 'album')
    # todo 胡金景，根据文本找到最佳匹配图片
    similar_key = []
    similar_value = []
    for filename in os.listdir(path0):
        if filename.endswith('jpg') or filename.endswith('png'):
            #  存储图片的文件夹绝对路径
            str1 = path0 + '\\' + filename
            print(str1)
            similar_key.append(str1)
            sim = match(str1, sent)
            # 将得到的多张图片匹配你输入的图片关键词
            similar_value.append(sim)
    # 存放图片绝对路径和图文相似度的字典
    similar_dict = dict(zip(similar_key, similar_value))
    print(similar_dict)
    similar_value.sort(reverse=True)
    print(similar_value)
    result = ' '
    # 找到图文相似度最高的那个图片的绝对路径
    for key, value in similar_dict.items():
        if value == similar_value[0]:
            result = key
            break
    url_list = img_path2url(result)
    return jsonify(url_list)
