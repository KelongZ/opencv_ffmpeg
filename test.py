import cv2
import os

WAIT = 3000
os.chdir('C:/Users/a3139/Desktop/PyCode/wx_images')
file_list = os.listdir()

fps = 30
# fourcc = cv2.VideoWriter_fourcc('I', '4', '2', '0')
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
videoWriter = cv2.VideoWriter(
    "../wx_article.mp4", fourcc, fps, (677, 968))

for i in range(len(file_list) -1):
    img1 = cv2.imread(file_list[i])

    # 每秒增加30帧图片以延长停顿时间
    frame = cv2.imread(file_list[i])
    for j in range(0, 45):
        videoWriter.write(frame)

    img2 = cv2.imread(file_list[i+1])
    src1 = cv2.resize(img1, (677, 968))
    src2 = cv2.resize(img2, (677, 968))

    for it in range(WAIT+1):
        if it % 100 == 0:
            weight = it / WAIT
            res = cv2.addWeighted(src1, 1-weight, src2, weight, 0)
            # cv2.imshow('images', res)
            # cv2.waitKey(20)

            videoWriter.write(res)

videoWriter.release()

# cv2.waitKey(0)
# cv2.destroyAllWindows()
