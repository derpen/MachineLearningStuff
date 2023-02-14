import torch
import os
from PIL import Image
from torch.utils.data import Dataset

class GetData(Dataset):
    def __init__(self, root_dir, transform=None):
        super(GetData, self).__init__()
        self.root_dir = root_dir
        self.transform = transform
        self.data = self.__load_data()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_path, label_path = self.data[idx]
        img = Image.open(img_path)
        with open(label_path, 'r') as f:
            first_line = f.readline()
            label = [float(x) for x in first_line.strip('\n').split()]
        
        if self.transform:
            img = self.transform(img)

        label = torch.tensor(label, dtype=torch.float32)

        return img, label
    
    def __load_data(self):
        data = []
        images_dir = os.path.join(self.root_dir, 'images')
        labels_dir = os.path.join(self.root_dir, 'labels')
        for filename in os.listdir(images_dir):
            img_path = os.path.join(images_dir, filename)
            label_path = os.path.join(labels_dir, os.path.splitext(filename)[0] + '.txt')
            if os.path.exists(label_path):
                data.append((img_path, label_path))
        
        return data