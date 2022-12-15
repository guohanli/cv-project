import json
import os

import torch
#import sys 
#sys.path.append("../..")

from utils import transform_image_bytes2tensor

current_path = os.path.dirname(__file__)
model = torch.jit.load(os.path.join(current_path, '..', '..', '..',
                                    'resource', 'densenet', 'densenet121.pt'))
model.eval()
imagenet_class_index = json.load(open(os.path.join(current_path, '..', '..', '..',
                                                   'resource', 'densenet', 'imagenet_class_index.json')))


def get_prediction(image_bytes):
    tensor = transform_image_bytes2tensor(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return imagenet_class_index[predicted_idx]


if __name__ == '__main__':
    with open("../../../resource/album/cat.png", 'rb') as f:
        image_bytes = f.read()
        print(get_prediction(image_bytes=image_bytes))
