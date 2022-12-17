import json

from facenet_pytorch.models.inception_resnet_v1 import InceptionResnetV1
from facenet_pytorch.models.mtcnn import MTCNN

from model.recognition.recognition import load_known_faces, match_faces
from utils import device, get_people_img_path_list, img_path_list_people_name_list, img_path_list2url_list, \
    generate_people_json_file, people_json_path, img_path2url


def generate_people_json():
    # mtcnn模型加载【设置网络参数，进行人脸检测】
    mtcnn = MTCNN(min_face_size=12, thresholds=[0.2, 0.2, 0.3], keep_all=True, device=device)
    # InceptionResnetV1模型加载【用于获取人脸特征向量】
    resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
    MatchThreshold = 1  # 人脸特征向量匹配阈值设置
    a = get_people_img_path_list()  # people list
    known_faces_emb, _ = load_known_faces(a[0], mtcnn, resnet)  # 已知人物图
    label = 1
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
        label = label + 1
        count.append(label)  # 总类别是c-1
    #count.pop()
    name = img_path_list_people_name_list(a)
    url_list = img_path_list2url_list(name)  # 'http://127.0.0.1:5000/angelababy1.png'
    # 创建一个只有people的json文件
    generate_people_json_file(url_list, count)
    return count,a,label

def handle_new_people_img(new_img_path):
    mtcnn = MTCNN(min_face_size=12, thresholds=[0.2, 0.2, 0.3], keep_all=True, device=device)
    # InceptionResnetV1模型加载【用于获取人脸特征向量】
    resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
    MatchThreshold = 1  # 人脸特征向量匹配阈值设置
    count,a,lable=generate_people_json()
    with open(people_json_path, 'r', encoding='utf8') as fp:
        people_data = json.load(fp)
    img_url_list, id_list = zip(*people_data)
    img_url_list, id_list = list(img_url_list),list()
    # c是最新的类别id，在没有相似图片的情况下直接给新图片用
    c = len(set(id_list)) + 2
    # todo 王婧馨，将新图片和之前的图片比较，得到id，赋值给new_img_category
    for i in range(len(id_list)):
        known_faces_emb, _ = load_known_faces(a[i], mtcnn, resnet)  # 已知人物图
        faces_emb, img = load_known_faces(new_img_path, mtcnn, resnet)#待测任务图
        isExistDst = match_faces(faces_emb, known_faces_emb, MatchThreshold)  # 人脸匹配
        if isExistDst:
            count.append(count[i])
        else:
            continue
    lable=lable+1
    count.append(lable)
    # pass
    new_img_category = count[-1]
    new_img_url = img_path2url(new_img_path)
    img_url_list.insert(0, new_img_url)
    id_list.insert(0, new_img_category)
    generate_people_json_file(img_url_list, id_list)


def handle_delete_people_img(img_path):
    with open(people_json_path, 'r', encoding='utf8') as fp:
        people_data = json.load(fp)
    img_url = img_path2url(img_path)
    people_data = list(filter(lambda x: x[0] != img_url, people_data))
    img_url_list, id_list = zip(*people_data)
    generate_people_json_file(img_url_list, id_list)


generate_people_json()