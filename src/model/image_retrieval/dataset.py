import torch
from PIL import Image
from torch.utils.data import Dataset, DataLoader
import  numpy as np
from torchvision.transforms import ToTensor
from torchvision import transforms, models
from torch import nn, optim
import os

class MyData(Dataset):
    def __init__(self, root_dir, model_name):
        self.root_dir = root_dir
        self.path = self.root_dir
        self.img_path = os.listdir(self.path)
        # print(self.img_path)
        for i in self.img_path:
            if i == 'query':
                self.img_path.remove('query')
        self.model_name = model_name

    def __getitem__(self, idx):
        img_name = self.img_path[idx]
        img_item_path = os.path.join(self.root_dir, img_name)
        # print(img_item_path)
        if self.model_name == "train":
            tf = transforms.Compose([
                transforms.Resize([640, 640]),
                transforms.RandomHorizontalFlip(p=0.5),
                transforms.ToTensor(),
                transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
            ])
        img = Image.open(img_item_path)
        img = tf(img)
        return img, img_name

    def __len__(self):
        return len(self.img_path)