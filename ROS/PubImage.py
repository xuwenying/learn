#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import rospy
from std_msgs.msg import String
from std_msgs.msg import Header
from sensor_msgs.msg import Image

import numpy as np # 引入numpy 用于矩阵运算
import cv2 # 引入opencv库函数
import time

## VideCapture里面的序号
# 0 : 默认为笔记本上的摄像头(如果有的话) / USB摄像头 webcam
# 1 : USB摄像头2
# 2 ：USB摄像头3 以此类推
# -1：代表最新插入的USB设备 


def GetCaptureImage():
    
    rospy.init_node('Camera', anonymous=True)
    image_pub = rospy.Publisher('/capImage/image_raw', Image, queue_size=10)

    image_data = cv2.imread('/home/xwy/develop/RosP_GetData/src/capture/image_data/bbb.jpeg')
    #print(image_data.shape,image_data[10,0,2])
    # 图像计数 从1开始
    img_count = 1

    # while(True):
    while not rospy.is_shutdown():
        ## 逐帧获取画面
        # 如果画面读取成功 ret=True，frame是读取到的图片对象(numpy的ndarray格式)
        ros_frame = Image()
        header = Header(stamp = rospy.Time.now())
        header.frame_id = "camera"
        ros_frame.header = header
        ros_frame.width = image_data.shape[1]
        ros_frame.height = image_data.shape[0]
        ros_frame.encoding = "bgr8"
        ros_frame.step = image_data.shape[1]*3
        ros_frame.data = np.array(image_data).tostring()
        # print(ros_frame.data)
        image_pub.publish(ros_frame)

        rate = rospy.Rate(10) # 10hz

        # 更新窗口“image_win”中的图片
        cv2.imshow('image_win',image_data)

        # 等待按键事件发生 等待1ms
        key = cv2.waitKey(1)
        if key == ord('q'):
            # 如果按键为q 代表quit 退出程序
            print("程序正常退出...Bye 不要想我哦")
            break
        elif key == ord('c'):
            ## 如果c键按下，则进行图片保存
            # 写入图片 并命名图片为 图片序号.png
            cv2.imwrite("{}.png".format(img_count), image_data)
            print("截图，并保存为  {}.png".format(img_count))
            # 图片编号计数自增1
            img_count += 1

    # 销毁所有的窗口
    cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        GetCaptureImage()
    except rospy.ROSInterruptException:
        pass
