import torch
import numpy as np
from PIL import Image
import albumentations as A
from albumentations.pytorch import ToTensorV2

from utils import modules

import json
import argparse
import matplotlib.pyplot as plt


with open("./idx2cls.json", "r") as f:
    idx2cls = json.load(f)

parser = argparse.ArgumentParser()
parser.add_argument('--image_path', type=str, default="", required=True, help="图片路径，例 123.jpg")
parser.add_argument('--device', type=str, default=None, help="推理设备，例 cpu, cuda")
args = parser.parse_args()
device = args.device
ROOT_PATH = args.image_path

if device is None:
    device = "cuda" if torch.cuda.is_available() else "cpu"
# device = "cuda"

IMAGE_SIZE = 420

transform = A.Compose([
    A.SmallestMaxSize(max_size=IMAGE_SIZE),
    A.CenterCrop(IMAGE_SIZE, IMAGE_SIZE),
    A.Normalize(),
    ToTensorV2()
])

img = np.array(Image.open(ROOT_PATH).convert("RGB"))
if transform is not None:
    img = transform(image=img)["image"]


model = modules.ConvNext(25, False)
model.load_state_dict(torch.load("./checkpoint/99866.pt", "cpu")["model"])
model.eval()
model.to(device)

with torch.no_grad():
    x = img.to(device).unsqueeze(0)
    out = model(x)
    logit = out.argmax(-1).cpu()

plt.imshow(Image.open(ROOT_PATH).convert("RGB"))
plt.title(f"Predict: {idx2cls[str(logit.item())]}")
plt.show()