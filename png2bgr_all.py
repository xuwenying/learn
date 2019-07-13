# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 10:25:39 2019

@author: wenying.xu
"""

import os
import cv2

array_of_img = [] # this if for store all of the image data
# this function is for read image,the input is directory name
directory_name="D:\\work\\ttt_245_1024_512\\test_picture\\png\\"
for filename in os.listdir(directory_name):
    print(filename) #just for test
    savefilename=filename.split('.')
    #img is used to store the image data 
    img = cv2.imread(directory_name + "/" +filename )
    bbb=img
    aaa=bbb.transpose(2,0,1)
    with open("D:\\work\\ttt_245_1024_512\\test_picture\\bgr\\"+savefilename[0],"wb") as f:
        f.write(aaa.tostring())
    #array_of_img.append(img)
    #print(img)
    #print(array_of_img)
"""
img=cv2.imread('D:\\work\\tidl_245_1024_512\\test_picture\\1024_512_png\\130.png')
bbb=img
aaa=bbb.transpose(2,0,1)
with open("D:\\work\\tidl_245_1024_512\\test_picture\\1024_512_bgr\\130","wb") as f:
    f.write(aaa.tostring())
    """
