import io
import json
import os
import linecache
import torch
from PIL import Image
from torchvision.transforms import transforms


"""
Some concepts.
img_path: just as '/Users/lgh/PycharmProjects/cv-project/resource/album/dog.jpeg'
img_name: just as 'dog.jpeg'
url_path: just as 'http://127.0.0.1:5000/dog.jpeg'
xxx_list: python list(like array in other language) with xxx as element
"""
port = 5000

current_path = os.path.dirname(__file__)
album_path = os.path.join(current_path, '..', 'resource', 'album')
meta_json_path = os.path.join(album_path, 'meta.json')
url_prefix = 'http://127.0.0.1:' + str(port) + '/'
default_transforms = transforms.Compose([transforms.Resize(255),
                                         transforms.CenterCrop(224),
                                         transforms.ToTensor(),
                                         transforms.Normalize(
                                             [0.485, 0.456, 0.406],
                                             [0.229, 0.224, 0.225])])


def get_img_name_list():
    img_name_list = []
    for root, dirs, files in os.walk(album_path):
        for file in files:
            if file.endswith("png") or file.endswith("jpg") or file.endswith("jpeg"):
                img_name_list.append(file)

    return img_name_list


def get_img_path_list():
    album_path = os.path.join(current_path, '..', 'resource', 'album')
    img_path_list = []
    for root, dirs, files in os.walk(album_path):
        for file in files:
            if file.endswith("png") or file.endswith("jpg") or file.endswith("jpeg"):
                img_path_list.append(os.path.abspath(os.path.join(root, file)))
    img_path_list = sorted(img_path_list, key=lambda x: os.path.getmtime(x), reverse=True)
    return img_path_list


def img_path2name(img_path):
    return os.path.basename(img_path)


def img_name2path(img_name):
    return os.path.abspath(os.path.join(album_path, img_name))


def img_path_list2name_list(img_path_list):
    return [img_path2name(img_path) for img_path in img_path_list]


def generate_meta_json_file(img_path_list, img_category_list):
    data = list(zip(img_path_list, img_category_list))
    with open(meta_json_path, 'w') as f:
        json.dump(data, f)


def get_img_path_list_for_certain_category(target_category):
    with open(meta_json_path, 'r') as f:
        path_category_list = json.load(f)
    result = []
    for (path, category) in path_category_list:
        if category == target_category:
            result.append(path)
    return result


def get_people_img_path_list():
    category = 'people'
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
    linecache.clearcache()
    return (path_list)


def img_path2url(img_path):
    img_name = os.path.basename(img_path)
    return url_prefix + img_name


def img_url2path(img_url):
    img_name = os.path.basename(img_url)
    return img_name2path(img_name)


def img_path_list2url_list(img_path_list):
    # this function not only works for img_path_list, but also for img_name_list
    return list(map(lambda x: img_path2url(x), img_path_list))


def _transform_PIL_image2tensor(image, custom_transforms=None):
    if custom_transforms is None:
        custom_transforms = default_transforms
    return custom_transforms(image).unsqueeze(0)


def transform_image_bytes2tensor(image_bytes, custom_transforms=None):
    image = Image.open(io.BytesIO(image_bytes))
    return _transform_PIL_image2tensor(image, custom_transforms)


def transform_image_path2tensor(img_path, custom_transforms=None):
    image = Image.open(img_path)
    return _transform_PIL_image2tensor(image, custom_transforms)


def transform_image_path_list2tensor(img_path_list, custom_transforms=None):
    result = []
    for img_path in img_path_list:
        result.append(transform_image_path2tensor(img_path, custom_transforms))
    return torch.cat(result, dim=0)


def delete_image_file(img_path):
    os.remove(img_path)


if __name__ == '__main__':
    img_name_list = get_img_name_list()
    print(img_name_list)

    img_path_list = get_img_path_list()
    print(img_path_list)

    print(img_path_list2name_list(img_path_list))

    generate_meta_json_file(img_path_list, ['cat', 'people', 'dog'])

    print(get_people_img_path_list())

    imgs = transform_image_path_list2tensor(img_path_list)
    print(imgs.shape)

    url_list = img_path_list2url_list(img_path_list)
    print(url_list)

    print(img_url2path(url_list[0]))
