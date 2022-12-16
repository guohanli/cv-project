import os

import torch
from facenet_pytorch.models.inception_resnet_v1 import InceptionResnetV1
from facenet_pytorch.models.mtcnn import MTCNN

from model.recognition.recognition import load_known_faces, match_faces
from utils import device, album_path, get_people_img_path_list, img_path_list_people_name_list, img_path_list2url_list, \
    generate_people_json_file


def generate_people_json():
    # mtcnn模型加载【设置网络参数，进行人脸检测】
    mtcnn = MTCNN(min_face_size=12, thresholds=[0.2, 0.2, 0.3], keep_all=True, device=device)
    # InceptionResnetV1模型加载【用于获取人脸特征向量】
    resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
    MatchThreshold = 1  # 人脸特征向量匹配阈值设置
    a = get_people_img_path_list()  # people list
    known_faces_emb, _ = load_known_faces(a[0], mtcnn, resnet)  # 已知人物图
    c = 1
    count = [1]
    for i in range(len(a) - 1):
        known_faces_emb, _ = load_known_faces(a[i + 1], mtcnn, resnet)  # 已知人物图
        for j in range(i + 1):
            faces_emb, img = load_known_faces(a[j], mtcnn, resnet)  # 待测任务图
            isExistDst = match_faces(faces_emb, known_faces_emb, MatchThreshold)  # 人脸匹配
            if isExistDst:
                count.append(count[j])
            else:
                continue
        c = c + 1
        count.append(c)  # 总类别是c-1
    count.pop()
    name = img_path_list_people_name_list(a)
    url_list = img_path_list2url_list(name)  # 'http://127.0.0.1:5000/angelababy1.png'
    # 创建一个只有people的json文件
    generate_people_json_file(url_list, count)
