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

def compute_color_for_id(label):
    """
    Simple function that adds fixed color depending on the id
    """
    palette = (2 ** 11 - 1, 2 ** 15 - 1, 2 ** 20 - 1)

    color = [int((p * (label ** 2 - label + 1)) % 255) for p in palette]
    return tuple(color)


obj_colors = {
    0: (0,255,255), #person
    #1: (255,0,0), # bicycle
    2: (0,255,0), # car
    #3: (6,140,201), #motorbike
    5: (255,51,51) #bus
}

classes = [0,2,5]
conf_threshold = 0.4
iou_threshold = 0.5

yolo_weights = 'yolov5m6.pt'

device = select_device('')

imgsz = 640

# Model
#model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model = attempt_load(yolo_weights, map_location=device)
model.conf = 0.25
model.classes = list(obj_colors.keys())
stride = int(model.stride.max())
imgsz = check_img_size(imgsz, s=stride) 
half = device.type != 'cpu'
fps_output = 25

classesFile = "vep.names"

source = 'video.mp4'
outputFile = 'result1.mp4'


cfg = get_config()
cfg.merge_from_file('deep_sort_pytorch/configs/deep_sort.yaml')
deepsort = DeepSort(cfg.DEEPSORT.REID_CKPT,
                        max_dist=cfg.DEEPSORT.MAX_DIST, min_confidence=cfg.DEEPSORT.MIN_CONFIDENCE,
                        nms_max_overlap=cfg.DEEPSORT.NMS_MAX_OVERLAP, max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
                        max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
                        use_cuda=True)


print('Video Detected')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter(outputFile, fourcc, 25, (1280,  720))


dataset = LoadImages(source, img_size=imgsz)
names = model.names

for frame_idx, (path, img, im0s, vid_cap) in enumerate(dataset):
        img = torch.from_numpy(img).to(device)
        #img = img.half() if half else img.float()  # uint8 to fp16/32
        img = img.float()
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        
        
        # Inference
        t1 = time_synchronized()*1000
        pred = model(img, augment=True)[0]
        pred = non_max_suppression(
            pred, conf_threshold, iou_threshold, classes, agnostic=False)
        t2 = time_synchronized()
        fps = (1000 / ((t2*1000)-t1))
        # Process detections
        for i, det in enumerate(pred):  # detections per image
            #if webcam:  # batch_size >= 1
            #    p, s, im0 = path[i], '%g: ' % i, im0s[i].copy()
            #else:
            p, s, im0 = path, '', im0s

            s += '%gx%g ' % img.shape[2:]  # print string
            #save_path = str(Path(out) / Path(p).name)

            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(
                    img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += '%g %ss, ' % (n, names[int(c)])  # add to string

                xywhs = xyxy2xywh(det[:, 0:4])
                confs = det[:, 4]
                clss = det[:, 5]

                # pass detections to deepsort
                outputs = deepsort.update(xywhs.cpu(), confs.cpu(), clss, im0)
                
                # draw boxes for visualization
                if len(outputs) > 0:
                    for j, (output, conf) in enumerate(zip(outputs, confs)): 
                        
                        bboxes = output[0:4]
                        id = output[4]
                        cls = output[5]

                        c = int(cls)  # integer class
                        label = f'{names[c]}: {id}'
                        color = compute_color_for_id(id)
                        plot_one_box(bboxes, im0, label=label, color=color, line_thickness=1)
                        cv2.putText(im0, "FPS: %.2f" % fps,
                                    (10,15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1, cv2.LINE_AA)

            else:
                deepsort.increment_ages()

            # Print time (inference + NMS)
            print('%sDone. (%.3fs)' % (s, t2 - t1))
            cv2.imshow(p, im0)
            #out.write(im0)
            if cv2.waitKey(1) == ord('q'):  # q to quit
              out.release()  
              raise StopIteration


    
    

# Inference

