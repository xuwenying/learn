#!/usr/bin/env python


import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

import numpy as np # 引入numpy 用于矩阵运算
import cv2 # 引入opencv库函数
import time



def callbackImage(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %d %d', data.width,data.height)
    # img = np.zeros((data.height, data.width, 3),dtype=np.uint8)
    image_data_ndarry = np.frombuffer(data.data,dtype=np.uint8)
    print(type(image_data_ndarry))
    cv_image = np.resize(image_data_ndarry, (data.height, data.width, 3))
    # cv_image = np.ndarray(shape=(data.height,data.width,3),dtype=np.uint8,buffer=data.data)
    # img[:,:,0], img[:,:,1],img[:,:,2] = cv_image
    print(cv_image.shape)
    cv2.imshow('image_win11',cv_image)
    img_count = 1
    # # 等待按键事件发生 等待1ms
    key = cv2.waitKey(1)


def GetImage():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('GetImage', anonymous=True)

    rospy.Subscriber('/capImage/image_raw', Image, callbackImage)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    GetImage()
