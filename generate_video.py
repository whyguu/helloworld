# -*- coding:utf8 -*-
import os
import cv2
import numpy as np
import glob


path = '/usr/data/gago_shihongxin/py-faster-rcnn/caffe-fast-rcnn/fuyu/data/results_video_v1'
filelist = os.listdir(path)
total_num = len(filelist)
# filelist = glob.glob(path+'/'+'tk_*.jpg')
# filelist.sort(key=lambda x:int(x[:-4]))
# print(filelist)
# video=cv2.VideoWriter("/home/gago/Documents/caffe-master/chifeng/data/video/VideoTest.avi", cv2.cv.CV_FOURCC('I','4','2','0'), 30, (500,800))
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
video=cv2.VideoWriter("/usr/data/gago_shihongxin/py-faster-rcnn/caffe-fast-rcnn/fuyu/data/video/fuyu_huasheng_v1.avi", fourcc, 300, (264,165))

for i in range(total_num):
    imgpath = os.path.join(path,'testpic_'+str(i)+'.jpg')
    img1 = cv2.imread(imgpath)
    print(imgpath)
    # img1 = cv2.resize(img1,(1000,1000))
    video.write(img1)
    # cv2.imshow("Image", img1)
    # key = cv2.waitKey(100)
# for item in filelist:
#     if item.endswith('.jpg'):
#         #item=path+'/'+item
#         img1 = cv2.imread(item)
#         print(item)
#         video.write(img1)
#         cv2.imshow("Image", img1)
#         key=cv2.waitKey(100)
#
video.release()
# cv2.destroyAllWindows()