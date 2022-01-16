#!/usr/bin/python
# -*- coding: utf-8 -*-

import shutil
from PIL import Image, ImageEnhance
import time
from pathlib import Path
from datetime import datetime
import ipaddress
import socket
import cv2
import torch
import torch.backends.cudnn as cudnn

obj_colors = {  # person
                # bicycle
                # car
                # motorbike
                # bus
                # truck
    0: (0, 0xFF, 0xFF),
    1: (0xFF, 0, 0),
    2: (0, 0xFF, 0),
    3: (6, 140, 201),
    4: (0xFF, 51, 51),
    5: (0, 0, 0xFF),
    }


def detectForVideo(file, model,output,ip_address,port):
    if(file == 'camera'):
        cap = cv2.VideoCapture(0)
    else:     
        cap = cv2.VideoCapture(file)
    (ret, img) = cap.read()

# ....scale_percent = 35 # percent of original size
# ....width = int(img.shape[1] * scale_percent / 100)
# ....height = int(img.shape[0] * scale_percent / 100)
# ....dim = (width, height)

    isip = False
    try:
        ip = ipaddress.ip_address(ip_address)
        isip = True
        sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
        print("IP address {} is valid. The object returned is {}".format(ip_address, ip))
    except ValueError:
        print("IP address {} is not valid".format(ip_address)) 


    while True:
        (ret, frame) = cap.read()

        # frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        # frame = iu.adjust_gamma(frame,4.0)....

        t1 = time.time() * 1000
        pred = model(frame, augment=True)
        results = pred.pandas().xyxy[0]

        # bounding_box = cv2.selectROI('Multi-Object Tracker', frame, True,False)


        results = results[results['class'].isin(obj_colors)]
        names = ",".join(results['name'].tolist())
        now = datetime.now()    
        current_time = now.strftime("%H:%M:%S")
        
        message = current_time + "|" + names
        with open(output, 'a') as f:
            f.write(message)
            f.write('\n')
        
        if(isip == True):
            sock.sendto((socket.gethostname()+ "|" + message).encode(), (ip_address, int(port)))
        
        for (index, row) in results.iterrows():

            (xmin, ymin, xmax, ymax) = (row['xmin'], row['ymin'], row['xmax'
                                        ], row['ymax'])
    
            cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax),
                          int(ymax)), obj_colors[row['class']], 1)
            cv2.rectangle(frame, (int(xmin), int(ymin) - 15), (int(xmax),
                          int(ymin)), obj_colors[row['class']], -1)
            cv2.putText(
                frame,
                row['name'] + ': ' + str(row['confidence']),
                (int(xmin), int(ymin) - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (0, 0, 0),
                4,
                cv2.LINE_AA,
                )
            cv2.putText(
                frame,
                row['name'] + ': ' + str(row['confidence']),
                (int(xmin), int(ymin) - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (0xFF, 0xFF, 0xFF),
                1,
                cv2.LINE_AA,
                )
    
        fps = 1000 / (time.time() * 1000 - t1)
        cv2.putText(
                frame,
                'FPS: %.2f' % fps,
                (10, 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0xFF, 0),
                1,
                cv2.LINE_AA,
                )
        
        cv2.imshow('frame', frame)
        
            #    out.write(frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
