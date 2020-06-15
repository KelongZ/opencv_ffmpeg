from PIL import Image
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


print("开始爬取")
# 创建chrome参数对象
options = webdriver.ChromeOptions()
options.add_argument('--headless')   # 无界面化.
options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
options.add_argument('--window-size=1920,1080')  # 指定浏览器窗口大小
options.add_argument('--start-maximized')  # 浏览器窗口最大化
options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
# options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片,加快访问速度
# options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
options.add_experimental_option(
    "excludeSwitches",
    ["ignore-certificate-errors","enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36')
# 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
# options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度

driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
      "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
driver.get('https://mp.weixin.qq.com/s?src=11&timestamp=1592030811&ver=2397&signature=bwfwaQuqImmAr6CLvbit88GkLSr3djvDW4HFHZGBZ3hBVCjtiFRNsM2nZathXOfmX40JoZnfsr97ERx8Ar2KRJx-LYdt8caP1X6rJhcusyaxCB6A4dryhxkPiVAU2b1B&new=1')
wx_img = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#img-content'))
)
time.sleep(0.5)
driver.save_screenshot("screenshot.png")  # 对整个浏览器页面进行截图
left = wx_img.location['x']
top = wx_img.location['y']
right = wx_img.location['x'] + wx_img.size['width']
bottom = 1000
all_page_px_length = wx_img.location['y'] + wx_img.size['height']
scoll_times = all_page_px_length//bottom

im = Image.open('screenshot.png')
im = im.crop((left, top, right, bottom))  # 对浏览器第一面截图进行裁剪
im.save('wx_images/wx0.png')

for i in range(scoll_times):
    """
    每次翻动页面截图
    """
    scrollTop_value = (i+1)*1000
    js = "var q=document.documentElement.scrollTop=%s" % (scrollTop_value)
    driver.execute_script(js)
    time.sleep(0.6)
    driver.save_screenshot("screenshot.png")
    im = Image.open('screenshot.png')
    im = im.crop((left, top, right, bottom))
    im.save('wx_images/wx'+str(i+1)+'.png')


driver.quit()
print("爬取完成")


from PIL import Image
from PIL import ImageFilter
import cv2
import numpy as np


# 处理图片，自动留白
def pic_handle(imgs_name, imgs_r_name):
    filename = imgs_name
    filename1 = imgs_r_name
    print(filename)
    print(filename1)
    # image = cv2.imdecode(np.fromfile(filename, dtype=np.uint8), -1)
    img = Image.open(filename, "r")
    image = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    # 双三次插值
    height, width = image.shape[:2]  # 获取原图像的水平方向尺寸和垂直方向尺寸。
    # 图片太瘦
    if height/width > 960/540:
        multemp = height/960
        res = cv2.resize(image, (int(width / multemp), 960), interpolation=cv2.INTER_AREA)
    # 图片太胖
    elif height/width < 960/540:
        multemp = width/540
        res = cv2.resize(image, (540, int(height / multemp)), interpolation=cv2.INTER_AREA)
    else:
        res = cv2.resize(image, (540, 960), interpolation=cv2.INTER_AREA)

    # 创建滤波器，使用不同的卷积核
    imgE = Image.fromarray(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
    gary2 = imgE.filter(ImageFilter.DETAIL)
    # #图像点运算
    gary3 = gary2.point(lambda i: i*0.9)
    img_convert_ndarray = cv2.cvtColor(np.asarray(gary3), cv2.COLOR_RGB2BGR)
    height1, width1 = img_convert_ndarray.shape[:2]
    temph = int((960 - height1)/2)
    tempw = int((540 - width1)/2)
    a = cv2.copyMakeBorder(img_convert_ndarray, temph, 960-temph-height1,tempw, 540-tempw-width1, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    cv2.imencode('.png', a)[1].tofile(filename1)  # 保存图片

# 开始做视频
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
    "output.avi", fourcc, fps, (540, 960))

im_names = os.listdir(img_root)
for im_name in range(len(im_names)):

    imgs_name = img_root+'wx'+str(im_name)+'.png'
    imgs_r_name = img_r_root+'wx'+str(im_name)+'.png'
    # 重新编辑图片
    pic_handle(imgs_name, imgs_r_name)

    frame = imread(imgs_name)
    frame_r = imread(imgs_r_name)

    videoWriter.write(frame)

videoWriter.release()

# dir = out_root.strip(".avi")
# command = "ffmpeg -i %s.avi %s.mp4" % (dir, dir)
# # m使用ffmped将avi压缩为mp4,注意两个的路径
# call(command.split())
