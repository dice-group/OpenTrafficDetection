import numpy as np
import cv2 as cv
import argparse


class OpticalFlow:
    
    def __init__(self):        
    # params for ShiTomasi corner detection
        self.feature_params = dict( maxCorners = 1000,
                       qualityLevel = 0.001,
                       minDistance = 7,
                       blockSize = 7 )
        
        # Parameters for lucas kanade optical flow
        self.lk_params = dict( winSize  = (15,15),
                          maxLevel = 2,
                          criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
        
        self.color = np.random.randint(0,255,(1000,3))
        
        self.green_color = np.array([0,255,0])
        self.red_color = np.array([0,0,255])
        
        
        self.p0 = None
        self.mask = None
        self.old_gray = None
        self.old_frame = None
        self.frame_threshold = 0
    
    
    def computeFeaturesToTrack(self,first_frame):
        self.old_frame = first_frame
        self.old_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)
        self.p0 = cv.goodFeaturesToTrack(self.old_gray, mask = None, **self.feature_params) 
        # Create a mask image for drawing purposes
        self.mask = np.zeros_like(self.old_frame)
        
        
    def computeOpticalFlow(self,frame):
        if(self.frame_threshold == 60):
            self.computeFeaturesToTrack(frame)
            self.frame_threshold = 0
            
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # calculate optical flow
        p1, st, err = cv.calcOpticalFlowPyrLK(self.old_gray, frame_gray, self.p0, None, **self.lk_params)
        # Select good points
        if p1 is not None:
            good_new = p1[st==1]
            good_old = self.p0[st==1]
        # draw the tracks
        for i,(new,old) in enumerate(zip(good_new, good_old)):
            a,b = new.ravel()
            c,d = old.ravel()
            self.mask = cv.line(self.mask, (int(a),int(b)),(int(c),int(d)), self.red_color.tolist(), 2)
            frame = cv.circle(frame,(int(a),int(b)),5,self.green_color.tolist(),-1)
        img = cv.add(frame,self.mask)
        self.old_gray = frame_gray.copy()
        self.p0 = good_new.reshape(-1,1,2)
        self.frame_threshold = self.frame_threshold + 1
        return img



