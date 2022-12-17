import cv2
import numpy as np
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1, extract_face
from utils import *

# 获得人脸特征向量
def load_known_faces(dstImgPath, mtcnn, resnet):
    aligned = []
    knownImg = cv2.imread(dstImgPath)  # 读取图片
    # img = Image.fromarray(cv2.cvtColor(knownImg, cv2.COLOR_BGR2RGB))
    boxes, probs, points = mtcnn.detect(knownImg, landmarks=True)
    face = mtcnn(knownImg)  # 使用mtcnn检测人脸，返回【人脸数组】
    if face is not None:
        aligned.append(face[0])
    aligned = torch.stack(aligned).to(device)
    with torch.no_grad():
        known_faces_emb = resnet(aligned).detach().cpu()  # 使用resnet模型获取人脸对应的特征向量


    # cv2.imshow('imshow', knownImg)
    # cv2.waitKey(0)
    return known_faces_emb, knownImg


# 计算人脸特征向量间的欧氏距离，设置阈值，判断是否为同一个人脸
def match_faces(faces_emb, known_faces_emb, threshold):
    isExistDst = False
    distance = (known_faces_emb[0] - faces_emb[0]).norm().item()
    #print("\n两张人脸的欧式距离为：%.2f" % distance)
    if (distance < threshold):
        isExistDst = True
    return isExistDst,distance



if __name__ == '__main__':
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
    MatchThreshold = 1.0  # 人脸特征向量匹配阈值设置
    #faces_emb, img = load_known_faces('E:/cv-project/resource/album/animate_pic/test.png', mtcnn, resnet)  # 待检测人物图

    #a=get_img_path_list_for_certain_category('people')
    a=get_people_img_path_list()#people list
    lable=1
    count=[1]
    for i in range(1,len(a)):
        known_faces_emb, _ = load_known_faces(a[i], mtcnn, resnet)  # 新进图
        flag=True
        for j in range(i):
            faces_emb, img = load_known_faces(a[j], mtcnn, resnet)#之前
            isExistDst,distance = match_faces(faces_emb, known_faces_emb, MatchThreshold)  # 人脸匹配
            print(i,j,isExistDst,distance)
            if isExistDst:
                count.append(count[j])
                print(count)
                flag=False
                break
        if flag:
            lable = lable + 1
            print(lable)
            count.append(lable)#总类别是lable-1
            print(count)
    #count.pop()
    name=img_path_list_people_name_list(a)
    url_list = img_path_list2url_list(name)#'http://127.0.0.1:5000/angelababy1.png'
    #创建一个只有people的json文件
    people=generate_people_json_file(url_list,count)
    with open(people_json_path, 'r', encoding='utf8') as fp:
        people_data = json.load(fp)
    img_path_list, id_list = zip(*people_data)
    all_id_type = set(id_list)
    #c = len(set(id_list)) + 1#图片总数

    # 返回一个类别的一张图片和id以及count
    # for i in range(1, c):
    #     result_list = []
    #     for i in range(c - 1):
    #         result_list.append([])
    #
    #     for i in range(1, c):
    #         url_path = get_peopleimg_path_list_for_certain_category(i)
    #         result_list[i - 1].append(url_path[0])
    #         result_list[i - 1].append(i)
    #         result_list[i - 1].append(len(get_peopleimg_path_list_for_certain_category(i)))
    #     result_list = list(map(lambda x: {'src': x[0], 'face_category_id': x[1], 'count': str(x[2])}, result_list))
    # print(result_list)
    with open(people_json_path, 'r', encoding='utf8') as fp:
        people_data = json.load(fp)
    img_path_list, id_list = zip(*people_data)
    all_id_type = set(id_list)
    #print(len(all_id_type))
    #c = len(set(id_list)) + 1
    # 返回一个类别的一张图片和id以及count
    i=0
    result_list = []
    for k in range(len(list(all_id_type))):#
        result_list.append ([])
    #     #result_list.append([])
    #     for j in range(2):
    #         result_list[k].append([])

    for id in all_id_type:
        url_path = get_peopleimg_path_list_for_certain_category(id)
        result_list[i].append(url_path[0])
        result_list[i].append(id)
        result_list[i].append(get_count_by_people_id(id, people_data))
        i=i+1
        if i==len(list(all_id_type)):
            break
    result_list = list(map(lambda x: {'src': x[0], 'face_category_id': x[1], 'count': str(x[2])}, result_list))

    print('第一个api')
    print(result_list)





    # #返回一个类别的所有图片
    #
    # face_category_id=1
    # result = list(
    #     map(lambda x: {'src': x[0], 'id': img_url2name(x[0])}, filter(lambda x: x[1] == face_category_id, people_data)))
    # print(result)
    #
    # # todo 王婧馨，将新图片和之前的图片比较，得到id，赋值给new_img_category
    # new_img_path='E:/cv-project/resource/img.png'
    # with open(people_json_path, 'r', encoding='utf8') as fp:
    #     people_data = json.load(fp)
    # img_url_list, id_list = zip(*people_data)
    # img_url_list, id_list = list(img_url_list), list(id_list)
    # #img_path = img_url2path(img_url_list)
    # # c是最新的类别id，在没有相似图片的情况下直接给新图片用
    # c = len(set(id_list)) + 1#+2
    # ##add
    # for i in range(len(img_url_list)):
    #     known_faces_emb, _ = load_known_faces(img_url2path(img_url_list[i]), mtcnn, resnet)  # 已知人物图
    #     faces_emb, img = load_known_faces(new_img_path, mtcnn, resnet)  # 待测任务图
    #     isExistDst = match_faces(faces_emb, known_faces_emb, MatchThreshold)  # 人脸匹配
    #     if isExistDst:
    #         id_list.append(id_list[i])
    #     else:
    #         continue
    # id_list.append(c)
    # # pass
    # new_img_category = id_list[-1]
    # new_img_url = img_path2url(new_img_path)
    # img_url_list.insert(0, new_img_url)
    # id_list.insert(0, new_img_category)
    # print(new_img_category,new_img_url)






