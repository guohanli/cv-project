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
    return isExistDst



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
    MatchThreshold = 1  # 人脸特征向量匹配阈值设置
    #faces_emb, img = load_known_faces('E:/cv-project/resource/album/animate_pic/test.png', mtcnn, resnet)  # 待检测人物图

    a=get_img_path_list_for_certain_category('people')
    #a=get_people_img_path_list()#people list
    known_faces_emb, _ = load_known_faces(a[0], mtcnn, resnet)  # 已知人物图
    c=1
    count=[1]
    for i in range(len(a)-1):
        known_faces_emb, _ = load_known_faces(a[i+1], mtcnn, resnet)  # 已知人物图
        for j in range(i+1):
            faces_emb, img = load_known_faces(a[j], mtcnn, resnet)#待测任务图
            isExistDst = match_faces(faces_emb, known_faces_emb, MatchThreshold)  # 人脸匹配
            if isExistDst:
                count.append(count[j])
            else:
                continue
        c=c+1
        count.append(c)#总类别是c-1
    count.pop()
    name=img_path_list_people_name_list(a)
    url_list = img_path_list2url_list(name)#'http://127.0.0.1:5000/angelababy1.png'
    #创建一个只有people的json文件
    people=generate_people_json_file(url_list,count)
    with open(people_json_path, 'r', encoding='utf8') as fp:
        people_data = json.load(fp)
    #返回一个类别的一张图片和id以及count
    list=[]
    for i in range (c-1):
        list.append([])

    for i in range(1,c):
        url_path=get_peopleimg_path_list_for_certain_category(i)
        list[i-1].append(url_path[0])
        list[i-1].append(i)
        list[i-1].append(len(get_peopleimg_path_list_for_certain_category(i)))
        #print(url_path[0],i,len(get_peopleimg_path_list_for_certain_category(i)))
    print(list)

    #返回一个类别的所有图片
    list1=[]
    for i in range(len(url_list)-1):
        list1.append([])

    for i in range(1,c):
        url_path=get_peopleimg_path_list_for_certain_category(i)
        for j in range (len(url_path)):
            img_name=img_url2path(url_path[j])
            name=img_path2name(img_name)
            list1[i-1].append(url_path[j])
            list1[i - 1].append(name)
            #print(url_path,name)
    print(list1)









