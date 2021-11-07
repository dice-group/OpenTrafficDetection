
import shutil
from PIL import Image, ImageEnhance
import time
from pathlib import Path
import cv2
import torch
import torch.backends.cudnn as cudnn


obj_colors = {
    0: (0,255,255), #person
    1: (255,0,0), # bicycle
    2: (0,255,0), # car
    3: (6,140,201), #motorbike
    4: (255,51,51), #bus
    5: (0,0,255) #truck
}


def detectForVideo(file,model):
	cap = cv2.VideoCapture(file)	
	ret, img = cap.read()
#	scale_percent = 35 # percent of original size
#	width = int(img.shape[1] * scale_percent / 100)
#	height = int(img.shape[0] * scale_percent / 100)
#	dim = (width, height)


	while (True):
	    ret, frame = cap.read()
	    	
	    #frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
	    #frame = iu.adjust_gamma(frame,4.0)	
	    t1 = time.time()*1000
	    pred = model(frame,augment=True)
	    results = pred.pandas().xyxy[0]
		
	    
	    
	    #bounding_box = cv2.selectROI('Multi-Object Tracker', frame, True,False)
	    
	#    print(bounding_box)
	    results = results[results['class'].isin(obj_colors)]
	    print(results)
	    for index, row in results.iterrows():   
		
		#xywhs = row[:, 0:4]
		
		#outputs = deepsort.update(xywhs.cpu(), confs.cpu(), clss, frame)
	    
                xmin,ymin,xmax,ymax = row['xmin'],row['ymin'],row['xmax'],row['ymax']
		
		
                cv2.rectangle(frame,(int(xmin),int(ymin)),(int(xmax),int(ymax)),obj_colors[row['class']],1)
                cv2.rectangle(frame,(int(xmin),int(ymin)-15),(int(xmax),int(ymin)),obj_colors[row['class']],-1)
                cv2.putText(frame, row['name'] + ': ' + str(row['confidence']),(int(xmin),int(ymin)-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 4, cv2.LINE_AA)
                cv2.putText(frame, row['name']+ ': ' + str(row['confidence']),(int(xmin),int(ymin)-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1,cv2.LINE_AA)
		
	    
	    fps = (1000 / ((time.time()*1000)-t1))
	    cv2.putText(frame, "FPS: %.2f" % fps,
	    (10,15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1, cv2.LINE_AA)
		
	    
	    cv2.imshow('frame',frame)
	#    out.write(frame)
	    if cv2.waitKey(1) & 0xFF == ord('q'):
		    cap.release()
		    cv2.destroyAllWindows()
		    break

def detectForCamera(model):
	vid = cv2.VideoCapture(0)
	ret, frame = vid.read()
	width = int(frame.shape[1] * 30 / 100)
	height = int(frame.shape[0] * 30 / 100)
	while (True):
            ret, frame = vid.read()
            frame = cv2.resize(frame, (width,height), interpolation = cv2.INTER_AREA)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)	
	    #frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
	    #frame = iu.adjust_gamma(frame,4.0)	
            t1 = time.time()*1000
            pred = model(frame,augment=True)
            results = pred.pandas().xyxy[0]
		
	    
	    
	    #bounding_box = cv2.selectROI('Multi-Object Tracker', frame, True,False)
	    
	#    print(bounding_box)
            results = results[results['class'].isin(obj_colors)]
            print(results)
            for index, row in results.iterrows():   
		
		#xywhs = row[:, 0:4]
		
		#outputs = deepsort.update(xywhs.cpu(), confs.cpu(), clss, frame)
	    
                xmin,ymin,xmax,ymax = row['xmin'],row['ymin'],row['xmax'],row['ymax']
		
		
                cv2.rectangle(frame,(int(xmin),int(ymin)),(int(xmax),int(ymax)),obj_colors[row['class']],1)
                cv2.rectangle(frame,(int(xmin),int(ymin)-15),(int(xmax),int(ymin)),obj_colors[row['class']],-1)
                cv2.putText(frame, row['name'] + ': ' + str(row['confidence']),(int(xmin),int(ymin)-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 4, cv2.LINE_AA)
                cv2.putText(frame, row['name']+ ': ' + str(row['confidence']),(int(xmin),int(ymin)-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1,cv2.LINE_AA)
		
	    
            fps = (1000 / ((time.time()*1000)-t1))
            cv2.putText(frame, "FPS: %.2f" % fps,
            (10,15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1, cv2.LINE_AA)
		
	    
            cv2.imshow('frame',frame)
	#    out.write(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
