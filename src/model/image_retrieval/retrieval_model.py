import dataset

import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import models


def image_retrieval(base_path, query_path, base_batch_size):
    base_dataset = dataset.MyData(base_path, 'train')
    query_dataset = dataset.MyData(query_path, 'train')

    base_loader = DataLoader(base_dataset, batch_size=base_batch_size, shuffle=False)
    query_loader = DataLoader(query_dataset, batch_size=1, shuffle=False)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(device, "*"*20)
    model = models.resnet101(weights=models.ResNet101_Weights.DEFAULT)
    model.to(device)

    features = []
    base_img_names = []
    for batch, (img, img_name) in enumerate(base_loader):
        img = img.to(device)
        feature = model(img)
        features.append(feature)

        p = list(img_name)
        base_img_names = p

    print(base_img_names)
    
    features_q = []
    for batch, (img, _) in enumerate(query_loader):
        img = img.to(device)
        feature = model(img)
        features_q.append(feature)

    query_feature = features_q[0][0]
    scores = {}

    # calculate similarity
    for i in range(len(features[0])):
        similarity = torch.cosine_similarity(query_feature, features[0][i], dim=0)
        img_name = base_img_names[i]
        scores[img_name] = similarity
    
    # print(scores)
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    scores_asc = dict(sorted_scores)
    print(scores_asc)
    return scores_asc

def getMaxSimilarity(scores):
    img_name = next(iter(scores))
    similar_score = scores.get(img_name)
    return img_name, similar_score

def getTopKSimilarity(scores, K):
    for i, (key, value) in scores.items():
        print(key, "score: ", value)
        if i > K:
            break


# if __name__ == '__main__':
#     img_path = '/public/home/CS272/liuwen-cs272/image_retrieval/my_image_retrieval/images/'
#     query_path = '/public/home/CS272/liuwen-cs272/image_retrieval/my_image_retrieval/images/query/'
#     scores = image_retrieval(base_path=img_path, query_path=query_path, base_batch_size=10)
#     img_name, max_score = getMaxSimilarity(scores)
#     print(img_name, max_score)
    