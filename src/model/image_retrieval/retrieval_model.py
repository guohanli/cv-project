import os
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import models

# import dataset
from model.image_retrieval import dataset

def image_retrieval(base_path, query_path, base_batch_size):
    base_dataset = dataset.MyData(base_path)
    query_dataset = dataset.QueryData(query_path)

    base_loader = DataLoader(base_dataset, batch_size=base_batch_size, shuffle=False)
    query_loader = DataLoader(query_dataset, batch_size=1, shuffle=False)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(device, "*"*20)
    model = models.resnet101(weights=models.ResNet101_Weights.DEFAULT)
    model.to(device)

    pre = False
    features = []
    base_img_names = []

    # just go through network
    if True: 
        for batch, (img, img_name) in enumerate(base_loader):
            img = img.to(device)
            base_features = model(img)
            features.append(base_features)

            p = list(img_name)
            base_img_names = p

        # # write base features into file
        # feature_txt = open("base_features.txt", mode='w')
        # feature_txt.writelines(str(features))
        # feature_txt.close()
        # print("saved features!")
        
    # else:
    #     # read features
    #     read_features = open("base_features.txt", mode='r')
    #     features = read_features.read()
    #     features = list(features)
    #     print(features)

    print(base_img_names)
    
    features_q = []
    for batch, img in enumerate(query_loader):
        img = img.to(device)
        query_feature = model(img)
        features_q.append(query_feature)

    similarity = batch_cosine_similarity(query_feature, base_features)
    # print(similarity)

    scores = similarity.tolist()
    # print(type(scores), scores)
    scores = scores[0]

    res = dict()
    for i in range(len(scores)):
        res[base_img_names[i]] = scores[i]

    sorted_scores = sorted(res.items(), key=lambda x: x[1], reverse=True)
    scores_asc = dict(sorted_scores)
    print(scores_asc)
    return scores_asc

    # query_feature = features_q[0][0]
    # scores = {}

    # calculate similarity
    # for i in range(len(features[0])):
    #     similarity = torch.cosine_similarity(query_feature, features[0][i], dim=0)
    #     img_name = base_img_names[i]
    #     scores[img_name] = similarity

    # # print(scores)
    # sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    # scores_asc = dict(sorted_scores)
    # print(scores_asc)
    # return scores_asc

def getMaxSimilarity(scores, query_name):
    # img_name = next(iter(scores))
    for key in scores:
        if key == query_name:
            print("equal! pass !")
            continue
        else:
            img_name = key
            similar_score = scores.get(img_name)
            break

    # if img_name is query_name:
    #     img_name = next(iter(scores))
    #     similar_score = scores.get(img_name)
    return img_name, similar_score


def getTopKSimilarity(scores, K):
    for i, (key, value) in scores.items():
        print(key, "score: ", value)
        if i > K:
            break

def batch_cosine_similarity(query, base):
    a_number = query.size(0)
    b_number = base.size(0)

    a_embedding = query.unsqueeze(1).repeat(1, b_number, 1).view(-1, 1000)
    b_embedding = base.unsqueeze(0).repeat(a_number, 1, 1).view(-1, 1000)

    similarity = torch.cosine_similarity(a_embedding, b_embedding)
    similarity = similarity.view(a_number, b_number)

    return similarity

# if __name__ == '__main__':
#     img_path = 'resource\images'
#     # img_path = the folder path of base images.
#     query_path = 'resource\images\query\Tower07.jpeg'
#     # query_path = the path of query image, only 1 image.
    
#     scores = image_retrieval(base_path=img_path, query_path=query_path, base_batch_size=10)
#     img_name, max_score = getMaxSimilarity(scores)
#     img_item_path = os.path.join(img_path, img_name)
#     image = Image.open(img_item_path)
#     image.show()
    