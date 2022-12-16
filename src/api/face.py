import cv2
from flask import Blueprint
from flask import jsonify, request

from model.recognition.filter import cartoon
from utils import *

face_api = Blueprint('face_api', __name__)


@face_api.route('/get_face_covers')
def get_face_covers():
    with open(people_json_path, 'r', encoding='utf8') as fp:
        people_data = json.load(fp)
    img_path_list, id_list = zip(*people_data)
    c = len(set(id_list)) + 1
    # 返回一个类别的一张图片和id以及count
    for i in range(1, c):
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
        result_list = list(map(lambda x: {'src': x[0], 'face_category_id': x[1], 'count': str(x[2])}, result_list))
    return jsonify(result_list)


@face_api.route('/get_somebody_faces')
def get_somebody_faces():
    face_category_id = int(request.args.get('face_category_id'))
    with open(people_json_path, 'r', encoding='utf8') as fp:
        people_data = json.load(fp)
    result = list(
        map(lambda x: {'src': x[0], 'id': img_url2name(x[0])}, filter(lambda x: x[1] == face_category_id, people_data)))
    return jsonify(result)


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
    img_animate_name = img_path2name(img_animate_path)
    img_animate_url = img_path2url(img_animate_path)
    return jsonify({'src': img_animate_url, 'id': img_animate_name})
