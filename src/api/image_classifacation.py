import os
import time
import json
from flask import Blueprint
from flask import jsonify, request
import utils

import sys 
sys.path.append("..")

from model.image_classification.detectmy_singleimg import get_single_img
import model.image_classification.detectmy
import linecache
import os



image_classification_api = Blueprint('image_classification_api', __name__)

#输出所有label为people的路径的list
def get_face_path():
    pathlist = get_label_path('people')
    return (pathlist)

#输入标签，输出它们所在的路径list
def get_label_path(category):
    
    current_path_data = os.path.dirname(__file__)   
    current_path_data = os.path.join(current_path_data,'..')
    label_path_data = os.path.join(current_path_data,'model','image_classification','data.txt')

    count=len(open(label_path_data,'r').readlines())
    print('count',count)

    i=1
    path_list = []
    while i<=count:
        text = linecache.getline(label_path_data,i)
        if_category_in = category in text
        if if_category_in:
            text1 = text.split('  ')[0]
            path_list.append(text1)
        i += 1
    return(path_list)


@image_classification_api.route('/new_image', methods=['POST'])
def new_image():
    file = request.files.get('new_image')
    file_name = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + '.jpeg'
    file_save_path = os.path.join(utils.album_path, file_name)
    file.save(file_save_path)
    get_single_img(file_name)
    return ''

@image_classification_api.route('/delete_image',methods=['POST'])
def delete_img():
    name = json.loads(request.data)

    delete_path = utils.img_name2path(name)
    utils.delete_image_file(delete_path)

    current_path_album = os.path.dirname(__file__)
    data_txt_path = os.path.join(current_path_album,'..','model','image_classification','data.txt')

    file = open(data_txt_path)
    lines = file.readlines()
    length = len(lines)

    i=0
    while i<length:
        text = linecache.getline(data_txt_path,i)
    
        if name in text:
            del lines[i-1]
            break

        i+=1
    file.close

    filenew = open(data_txt_path,'w')
    filenew.writelines(lines)
    filenew.close()
    return ""
    



@image_classification_api.route('/get_covers')
def get_covers():

    lists = []
    current_path_album = os.path.dirname(__file__)
    data_txt_path = os.path.join(current_path_album,'..','model','image_classification','data.txt')
    length = len(linecache.getlines)

    j=1
    types = []
    while j<=length:
        type = linecache.getline(data_txt_path,j)
        type = type.split('  ')[1]
        types.append(type)

    types = list(set(types))

    #types = ['people','animal','fruit','bicycle']
    
    for i in types:
        print('i',i)
        covers = get_label_path(i)
        
        coverss = covers[0]
        dict = {'img_path':utils.img_path2url(coverss),'category':i}
        lists.append(dict)

    return jsonify(lists)
    '''
    return jsonify([{'img_path': 'http://127.0.0.1:5000/jack.png', 'category': 'people'},
                    {'img_path': 'http://127.0.0.1:5000/cat.png', 'category': 'animal'}])
    '''


@image_classification_api.route('/get_category_imgs')
def get_category_imgs():
    category = request.args.get("category")
    # todo 邱佳存，根据种类找到对应的图片数组
    


    '''
    #获取label文件路径
    current_path_data = os.path.dirname(__file__)
    #print('11111111111111111',current_path_data)
    current_path_data = os.path.join(current_path_data,'..')
    #print(current_path_data)
    label_path_data = os.path.join(current_path_data,'model','image_classification','data.txt')  

    #获取文件行数
    count=len(open(label_path_data,'r').readlines())
    print('count',count)

    #将指定label图片的路径全部找出
    i=1
    path_list = []
    while i<=count:
        text = linecache.getline(label_path_data,i)
        if_category_in = category in text
        if if_category_in:
            text1 = text.split('  ')[0]
            path_list.append(text1)
        i += 1
    '''
    
    path_list = get_label_path(category)
    output_path_list = []
    j = 0
    while j<len(path_list):
        dict = {'src':utils.img_path2url(path_list[j]),'id':os.path.basename(path_list[j])}
        output_path_list.append(dict)
        j = j+1
    
    return jsonify(output_path_list)

    '''
    return jsonify(
        [{'src': 'http://127.0.0.1:5000/jack.png', 'id': 'jack.png'},
         {'src': 'http://127.0.0.1:5000/cat.png', 'id': 'cat.png'},
         {'src': 'http://127.0.0.1:5000/dog.jpeg', 'id': 'dog.jpeg'},
         {'src': 'http://127.0.0.1:5000/jack.png', 'id': 'jack.png'},
         {'src': 'http://127.0.0.1:5000/cat.png', 'id': 'cat.png'},
         {'src': 'http://127.0.0.1:5000/dog.jpeg', 'id': 'dog.jpeg'}])
    '''

if __name__ == '__main__':
    lists = get_face_path()
    print(lists)