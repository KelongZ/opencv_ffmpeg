from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize, INTER_AREA
import os
from subprocess import call

img_root = "wx_images/"
img_r_root = "wx_images_r/"
# out_root = "C:/Users/Administrator/Desktop/数据可视化python/wx_pics/output.avi"
# Edit each frame's appearing time!
fps = 1
fourcc = VideoWriter_fourcc('I', '4', '2', '0')
videoWriter = VideoWriter(
    "output.avi", fourcc, fps, (677, 968))

im_names = os.listdir(img_root)
for im_name in range(len(im_names)):

    imgs_name = img_root+'wx'+str(im_name)+'.png'
    imgs_r_name = img_r_root+'wx'+str(im_name)+'.png'
    # 重新编辑图片
    # pic_handle(imgs_name, imgs_r_name)

    frame = imread(imgs_name)
    frame_r = imread(imgs_r_name)

    videoWriter.write(frame)

videoWriter.release()
