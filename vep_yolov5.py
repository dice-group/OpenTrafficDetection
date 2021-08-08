import sys
sys.path.insert(0, './yolov5')

from yolov5.utils.google_utils import attempt_download
from yolov5.models.experimental import attempt_load
from yolov5.utils.datasets import LoadImages, LoadStreams
from yolov5.utils.general import check_img_size, non_max_suppression, scale_coords, check_imshow, xyxy2xywh
from yolov5.utils.torch_utils import select_device, time_synchronized
from yolov5.utils.plots import plot_one_box
from deep_sort_pytorch.utils.parser import get_config
from deep_sort_pytorch.deep_sort import DeepSort
import argparse
import os
import platform
import shutil
import time
from pathlib import Path
import cv2
import torch
import torch.backends.cudnn as cudnn


obj_colors = {
    0: (0,255,255), #person
    #1: (255,0,0), # bicycle
    2: (0,255,0), # car
    #3: (6,140,201), #motorbike
    5: (255,51,51) #bus
}

yolo_weights = 'yolov5/weights/yolov5s.pt'

device = select_device('')

# Model
#model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model = attempt_load(yolo_weights, map_location=device)
model.conf = 0.25
model.classes = list(obj_colors.keys())
stride = int(model.stride.max())
fps_output = 25

classesFile = "vep.names"

file = 'video.mp4'
outputFile = 'result1.mp4'


cfg = get_config()
cfg.merge_from_file('deep_sort_pytorch/configs/deep_sort.yaml')
deepsort = DeepSort(cfg.DEEPSORT.REID_CKPT,
                        max_dist=cfg.DEEPSORT.MAX_DIST, min_confidence=cfg.DEEPSORT.MIN_CONFIDENCE,
                        nms_max_overlap=cfg.DEEPSORT.NMS_MAX_OVERLAP, max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
                        max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
                        use_cuda=True)


print('Video Detected')
cap = cv2.VideoCapture(file)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(outputFile, fourcc, 25, (1280,  720))
ret, img = cap.read()

detected = False

while cap.isOpened():
    ret, frame = cap.read()
    img = torch.from_numpy(frame).to(device)
    t1 = time.time()*1000
    pred = model(img,augment=True)
    results = pred.pandas().xyxy[0]
    
    
    #bounding_box = cv2.selectROI('Multi-Object Tracker', frame, True,False)
    
    #print(bounding_box)
    #results = results[results['class'].isin(obj_colors)]
    #print(results)
    for index, row in results.iterrows():   
        
        #xywhs = row[:, 0:4]
        
        #outputs = deepsort.update(xywhs.cpu(), confs.cpu(), clss, frame)
    
        xmin,ymin,xmax,ymax = row['xmin'], row['ymin'],row['xmax'], row['ymax']
        
        
        cv2.rectangle(frame,(int(xmin),int(ymin)),(int(xmax),int(ymax)),obj_colors[row['class']],1)
        cv2.rectangle(frame,(int(xmin),int(ymin)-15),(int(xmax),int(ymin)),obj_colors[row['class']],-1)
        cv2.putText(frame, row['name'] + ': ' + str(row['confidence']),
                   (int(xmin),int(ymin)-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 4, cv2.LINE_AA)
        cv2.putText(frame, row['name']+ ': ' + str(row['confidence']),
                   (int(xmin),int(ymin)-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        
    
    fps = (1000 / ((time.time()*1000)-t1))
    cv2.putText(frame, "FPS: %.2f" % fps,
    (10,15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1, cv2.LINE_AA)
        
    
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
    
    

# Inference

