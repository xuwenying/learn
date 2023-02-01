import numpy as np
import cv2


def read_rgb(file_path):
    rawImg= np.fromfile(file_path,dtype=np.uint8)
    # rawImg=rawImg.reshape(1536,1920,3)
    # rawImg = cv2.cvtColor(rawImg,cv2.COLOR_RGB2BGR)

    # rawImg=rawImg.reshape(1080,1920,4)
    # rawImg = cv2.cvtColor(rawImg,cv2.COLOR_RGBA2BGR)

    # rawImg=rawImg.reshape(768,960,4)
    # rawImg = cv2.cvtColor(rawImg,cv2.COLOR_RGBA2BGR)
    rawImg=rawImg.reshape(540,960,3)
    rawImg = cv2.cvtColor(rawImg,cv2.COLOR_RGB2BGR)
    cv2.imwrite('0.jpg',rawImg)



if __name__=="__main__":
    #write_rgb("car.jpg")
    #read_rgb("./resize.rgb")
    read_rgb("./0.rgb")
    # read_rgb("./remap0.rgb")
    # read_rgb("./resize_all.raw")
