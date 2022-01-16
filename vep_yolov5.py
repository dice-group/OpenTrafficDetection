import sys
sys.path.insert(0, './yolov5')

import argparse
import os
import platform
import shutil
from PIL import Image, ImageEnhance
from render_detect import detectForVideo
import time
from pathlib import Path
import cv2
import torch
import torch.backends.cudnn as cudnn

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=str, default='camera', help='source video (camera or videofile)')
parser.add_argument('--output', type=str, default='output_detection.txt', required=False,help='file output')
parser.add_argument('--remote_server', type=str, required=False,help='ip and port to send results')

args = parser.parse_args()

# Model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5_vep')
model = torch.hub.load('yolov5_config/', 'custom', path='yolov5_config/weights/best.pt', source='local') 
model.conf = 0.5
file = args.source

if(args.remote_server != None):
	ip,port = args.remote_server.split(":")
else:
	ip,port = ''

if(file == 'camera'):
	detectForVideo('camera',model,args.output,ip,port)
else:
	detectForVideo(file, model,args.output,ip,port)

# Inference

