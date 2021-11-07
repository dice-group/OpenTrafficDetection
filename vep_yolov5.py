import sys
sys.path.insert(0, './yolov5')

import argparse
import os
import platform
import shutil
from PIL import Image, ImageEnhance
from render_detect import detectForVideo
from render_detect import detectForCamera
import time
from pathlib import Path
import cv2
import torch
import torch.backends.cudnn as cudnn





parser = argparse.ArgumentParser()
parser.add_argument('--source', type=str, default='camera', help='source')


args = parser.parse_args()


# Model
#model = torch.hub.load('ultralytics/yolov5', 'yolov5_vep')
model = torch.hub.load('yolov5_config/', 'custom', path='yolov5_config/weights/yolov5_vep.pt', source='local') 
model.conf = 0.5
file = args.source
if(file == 'camera'):
	detectForCamera(model)
else:
	detectForVideo(file,model)









   
    

# Inference

