#!/usr/bin/env python
import cv2
vc = cv2.VideoCapture("test.mp4")
c = 1
if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False
while rval:
    cv2.imwrite('pics/'+str(c)+'.jpg', frame)
    rval, frame = vc.read()
    c = c+1
    cv2.waitKey(1)
vc.release()
