import cv2
from facenet_pytorch import MTCNN, InceptionResnetV1
from flask import Blueprint
from flask import jsonify, request

from model.recognition.filter import cartoon
from model.recognition.recognition import match_faces, load_known_faces
from utils import *

face_api = Blueprint('face_api', __name__)


@face_api.route('/get_face_covers')
def get_face_covers():
    # help(MTCNN)
    # help(InceptionResnetV1)
    # 获取设备
    album_path = os.path.join(current_path, '..', 'resource', 'album')
    people_json_path = os.path.join(album_path, 'people.json')
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print(device)
    # mtcnn模型加载【设置网络参数，进行人脸检测】
    mtcnn = MTCNN(min_face_size=12, thresholds=[0.2, 0.2, 0.3], keep_all=True, device=device)

    # InceptionResnetV1模型加载【用于获取人脸特征向量】
    resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
    MatchThreshold = 1  # 人脸特征向量匹配阈值设置
    # faces_emb, img = load_known_faces('E:/cv-project/resource/album/animate_pic/test.png', mtcnn, resnet)  # 待检测人物图

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
    people = generate_people_json_file(url_list, count)
    with open(people_json_path, 'r', encoding='utf8') as fp:
        people_data = json.load(fp)
    # 返回一个类别的一张图片和id以及count
    for i in range(1, c):
        url_path = get_peopleimg_path_list_for_certain_category(i)
        # print(url_path[0],i,len(get_peopleimg_path_list_for_certain_category(i)))
        result_list = []
        for i in range(c - 1):
            result_list.append([])

        for i in range(1, c):
            url_path = get_peopleimg_path_list_for_certain_category(i)
            result_list[i - 1].append(url_path[0])
            result_list[i - 1].append(i)
            result_list[i - 1].append(len(get_peopleimg_path_list_for_certain_category(i)))
            print(url_path[0], i, len(get_peopleimg_path_list_for_certain_category(i)))
        print(result_list)
        result_list = list(map(lambda x: {'src': x[0], 'url_path': x[1], 'count': x[2]}, result_list))
    return jsonify(result_list)
    # return jsonify([{'src': url_path[0], 'face_category_id':i, 'count':len(get_peopleimg_path_list_for_certain_category(i))}])


@face_api.route('/get_somebody_faces')
def get_somebody_faces():
    # todo 王婧馨
    # help(MTCNN)
    # help(InceptionResnetV1)
    # 获取设备
    face_category_id = request.args.get('face_category_id')
    album_path = os.path.join(current_path, '..', 'resource', 'album')
    people_json_path = os.path.join(album_path, 'people.json')
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print(device)
    # mtcnn模型加载【设置网络参数，进行人脸检测】
    mtcnn = MTCNN(min_face_size=12, thresholds=[0.2, 0.2, 0.3], keep_all=True, device=device)

    # InceptionResnetV1模型加载【用于获取人脸特征向量】
    resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
    MatchThreshold = 1  # 人脸特征向量匹配阈值设置
    # faces_emb, img = load_known_faces('E:/cv-project/resource/album/animate_pic/test.png', mtcnn, resnet)  # 待检测人物图

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
    people = generate_people_json_file(url_list, count)
    with open(people_json_path, 'r', encoding='utf8') as fp:
        people_data = json.load(fp)
    list1 = []
    for i in range(len(url_list) - 1):
        list1.append([])

    for i in range(1, c):
        url_path = get_peopleimg_path_list_for_certain_category(i)
        for j in range(len(url_path)):
            img_name = img_url2path(url_path[j])
            name = img_path2name(img_name)
            list1[i - 1].append(url_path[j])
            list1[i - 1].append(name)
            # print(url_path,name)
        # print(list1)
        return jsonify(list1)


@face_api.route('/get_animate')
def get_animate():
    img_url = request.args.get("img_url")
    img_path = img_url2path(img_url)
    img_name = img_path2name(img_path)
    # todo 王婧馨，获取生成的动画图片的路径
    img_path = os.path.join(album_path, 'man1.png')
    animate_path = os.path.join(current_path, '..', 'resource')
    save_path = os.path.join(animate_path, 'animate_pic', 'animate_man1.png')
    print(img_path)
    img = cv2.imread(img_path)
    # img=cv2.imread('E:/cv-project/resource/album/man1.png')
    # img = cv2.imread(img_path)
    dst_color = cartoon(img)
    imgnew = cv2.flip(dst_color, 1)
    # dst_color=old_pic(img)
    # cv2.imshow('img_color', dst_color)
    # cv2.waitKey()
    cv2.imwrite(save_path, imgnew)
    img_animate_path = save_path
    img_animate_name = img_name2path(img_animate_path)
    img_animate_url = img_path2url(img_animate_path)
    return jsonify({'src': img_animate_url, 'id': img_animate_name})
