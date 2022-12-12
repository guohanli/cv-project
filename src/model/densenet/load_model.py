import io
import json

import torch
import torchvision.transforms as transforms
from PIL import Image

model = torch.jit.load('resource/densenet/densenet121.pt')
model.eval()
imagenet_class_index = json.load(open('resource/densenet/imagenet_class_index.json'))


def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)


def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return imagenet_class_index[predicted_idx]


if __name__ == '__main__':
    with open("../../../resource/album/cat.png", 'rb') as f:
        image_bytes = f.read()
        print(get_prediction(image_bytes=image_bytes))
