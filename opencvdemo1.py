import cv2
from cv2 import VideoWriter,VideoWriter_fourcc,imread,resize
import os

videoCapture = cv2.VideoCapture("test.mp4")

img_root = "pics/"
# Edit each frame's appearing time!
fps = 20
fourcc = VideoWriter_fourcc(*"MJPG")
videoWriter = cv2.VideoWriter(
    "output.avi", fourcc, fps, (540, 960))

im_names = os.listdir(img_root)
for im_name in range(len(im_names)):
    frame = cv2.imread(img_root+str(im_name)+'.jpg')
    print(img_root+str(im_name)+'.jpg')
    videoWriter.write(frame)

videoWriter.release()
