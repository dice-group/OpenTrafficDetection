import cv2
import numpy as np

alpha = 0.7

obj_colors = {
    0: (0,255,255), #person
    1: (255,0,0), # bicycle
    2: (0,255,0), # car
    3: (6,140,201), #motorbike
    5: (255,51,51) #bus
}

frame_precision = {
    0: [],
    1: []
    #2: [],
    #3: [],
    #5: [],
    #7: []
}

overall_precision = {
    0: [],
    1: []
    #2: [],
    #3: [],
    #5: [],
    #7: []
}

def cleanFramePrecision():
    for key,value in frame_precision.items():
        frame_precision[key].clear()


def printFramePrecision(output,classNames):
    cv2.putText(output, "Frame Precision: ",
                (10, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 4, cv2.LINE_AA)
    cv2.putText(output, "Frame Precision: ",
                (10, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.putText(output, "Overall Precision: ",
                (290, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 4, cv2.LINE_AA)
    cv2.putText(output, "Overall Precision: ",
                (290, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 1, cv2.LINE_AA)
    y = 35
    for key, value in frame_precision.items():
        if value:
            cv2.putText(output,
                        f'{classNames[key].upper() + ": "}{"{:.2f}".format(sum(frame_precision[key]) / len(frame_precision[key]))}%',
                        (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 4, cv2.LINE_AA)
            cv2.putText(output,
                        f'{classNames[key].upper() + ": "}{"{:.2f}".format(sum(frame_precision[key]) / len(frame_precision[key]))}%',
                        (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
            y = y + 20
    y = 35
    for key,value in overall_precision.items():
        if value:
            cv2.putText(output,
                        f'{classNames[key].upper() + ": "}{"{:.2f}".format(sum(overall_precision[key]) / len(overall_precision[key]))}%',
                        (290, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 4, cv2.LINE_AA)
            cv2.putText(output,
                        f'{classNames[key].upper() + ": "}{"{:.2f}".format(sum(overall_precision[key]) / len(overall_precision[key]))}%',
                        (290, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
            y = y + 20
    cleanFramePrecision()


def findObjects(outputs,img,confThreshold,nmsThreshold,classNames):
    hT,wT,cT = img.shape
    overlay = img.copy()
    bbox =[]
    classIds = []
    confs =[]
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                w,h = int(det[2] * wT), int(det[3] * hT)
                x,y = int((det[0] * wT) - w/2), int((det[1] * hT) - h/2)
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confs.append(float(confidence))
    indices = cv2.dnn.NMSBoxes(bbox,confs,confThreshold,nmsThreshold)

    for i in indices:
        i = i[0]
        box = bbox[i]
        x,y,w,h = box[0],box[1],box[2],box[3]

        #if classIds[i] in frame_precision:
            #frame_precision[classIds[i]].append(confs[i] * 100)
            #overall_precision[classIds[i]].append(confs[i] * 100)

        if classIds[i] in obj_colors:
            cv2.rectangle(img,(x,y),(x+w,y+h),obj_colors[classIds[i]],-1)
        else:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),-1)
    output = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
    #Macro Recall
    #printFramePrecision(output,classNames)

    #Classes precision
    for i in indices:
        i = i[0]
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        cv2.putText(output, f'{classNames[classIds[i]].upper()}',
                    (x, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 4, cv2.LINE_AA)
        cv2.putText(output, f'{classNames[classIds[i]].upper()}',
                    (x, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

    return output

def resizeImage(img, scale_percent):
    #scale_percent = 100  # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return img
