import cv2

import detect as dt
import optical_flow as of
import image_utils as iu
import magic
import sys
import time
import argparse

classesFile = "vep.names"
wht = 448
confThreshold = 0.001
nmsThreshold = 0.01

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=str, default='0', help='source')
parser.add_argument('--output', type=str, default='result.mp4', help='output')



args = parser.parse_args()

file = args.source
outputFile = args.output
f = magic.Magic(mime=True, uncompress=True)
if file == 'camera':
	mimetype = 'camera'
else:
	mimetype = f.from_file(file)


model_cfg = 'config/yolov4/yolov4-vep_448.cfg'
model_w = 'config/yolov4/448/yolov4-vep_448_best.weights'

#model_cfg = 'config/yolov3/spp/yolov3-spp.cfg'
#model_w = 'config/yolov3/spp/yolov3-spp.weights'

classNames = []
with open(classesFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

#net = cv2.dnn.readNetFromDarknet(model_cfg,model_w)
net = cv2.dnn.readNet(model_w,model_cfg)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

layerNames = net.getLayerNames()
outputNames = [layerNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


if 'image' in mimetype:
    print('Image Detected')
    img = cv2.imread(file)
    img = dt.resizeImage(img,100)
    blob = cv2.dnn.blobFromImage(img, 1 / 255, (wht, wht), [0, 0, 0], 1, crop=False)
    net.setInput(blob)
    outputs = net.forward(outputNames)
    #print(outputNames)

    img = dt.findObjects(outputs, img, confThreshold, nmsThreshold, classNames)
     

    # out.write(img)
    while True:
        cv2.namedWindow("frame", cv2.WINDOW_AUTOSIZE)
        cv2.imshow('frame', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite(outputFile, img, [cv2.IMWRITE_JPEG_QUALITY, 100])
            break
elif mimetype == 'camera':
	print("Camera Detected")
	cap = cv2.VideoCapture(0)
	
	while(True):
	    # Capture frame-by-frame
	    ret, frame = cap.read()

	    frame = iu.adjust_gamma(frame,4.0)
	    blob = cv2.dnn.blobFromImage(frame, 1 / 255, (wht, wht), [0, 0, 0], 1, crop=False)
	    net.setInput(blob)
	    outputs = net.forward(outputNames)
	    frame = dt.findObjects(outputs, frame, confThreshold, nmsThreshold, classNames)

	    # Display the resulting frame
	    cv2.imshow('frame',frame)
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	    	cap.release()
	    	cv2.destroyAllWindows()
	    	break
		# When everything done, release the capture

else:
    print('Video Detected')
    cap = cv2.VideoCapture(file)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(outputFile, fourcc, 20.0, (1280,  720))
    fps = 25
    ret, img = cap.read()
    while cap.isOpened():
        ret, img = cap.read()
        t1 = time.time()*1000
        img = dt.resizeImage(img,100)
        blob = cv2.dnn.blobFromImage(img, 1 / 255, (wht, wht), [0, 0, 0], 1, crop=False)
        net.setInput(blob)
        outputs = net.forward(outputNames)
        img = dt.findObjects(outputs, img, confThreshold, nmsThreshold, classNames)
        t2 = (1000 / ((time.time()*1000)-t1))
        print("FPS: %.2f" % t2)
        cv2.imshow('frame', img)
        out.write(img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break


