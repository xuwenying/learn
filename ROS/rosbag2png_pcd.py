#!/usr/bin/python2
#coding:utf-8


import glob, os
import rosbag
import cv2
from cv_bridge import CvBridge, CvBridgeError
import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import Image
import numpy as np  
import pandas as pd

def bag2pcd_img(bagpath, image_topic, point_topic):
    IMAGE_SIZE = 1920*1080*3
    bridge = CvBridge()
    for f in glob.glob(bagpath + "/*.bag"):
        print("bagfile:",f)
        img_path = os.path.dirname(f) + "/" + os.path.split(f)[-1][:-4] + "/jpg"
        pcd_path = os.path.dirname(f) + "/" + os.path.split(f)[-1][:-4] + "/pcd"

        if not os.path.exists(img_path):
            os.makedirs(img_path, mode=0o777)

        if not os.path.exists(pcd_path):
            os.makedirs(pcd_path, mode=0o777)
        
        with rosbag.Bag(f, 'r') as bag:
            count = 0
            for topic, msg, t in bag.read_messages():
                print(topic, t, len(msg.data))
                # if topic == image_topic and count > 200:
                print(len(msg.data))
                if topic == image_topic:
                    try:
                        if (len(msg.data)>50000):
                            # print(msg.height,msg.width)  
                            #sensor_msgs::Image message to an OpenCV: bridege.imgmsg_to_cv2
                            # cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
                            cv_image = bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
                            # cv2.imshow("window", cv_image)           
                            # image_name = "lidar_img_%d" % msg.header.seq + ".jpg"
                            image_name = "lidar_img_%lf" % msg.header.stamp.to_sec()  + '.jpg'

                            file_path = os.path.join(img_path, image_name)
                            cv2.imwrite(file_path, cv_image)
                        else:
                            print("loss  loss  loss  img  !!!", )
                    except CvBridgeError as e:
                        print(e)
                        continue
                    print("img saved done !!!", )
                if topic == point_topic:
                    count += 1
                    data = pc2.read_points(msg)
                    points = np.array(list(data), dtype=np.float32)
                    df = pd.DataFrame(points)
                    df.dropna(axis=0, how='any', inplace=True)
                    points = np.array(df)
                    # abc = (msg.header.stamp.to_sec() + msg.header.stamp.nsec()/1e9)
                    # print abc
                    # filename = "%.6f" % msg.header.stamp.to_sec() + '.pcd'
                    filename = "lidar_data_GT_%lf" % msg.header.stamp.to_sec()  + '.pcd'
                    file_path = os.path.join(pcd_path, filename)
                    # points.tofile(file_path)
                    # print(file_path)
                    header = ['# .PCD v0.7 - Point Cloud Data file format\n',
                                'VERSION 0.7\n',
                                'FIELDS x y z intensity\n',
                                'SIZE 4 4 4 4\n',
                                'TYPE F F F F\n',
                                'COUNT 1 1 1 1\n',
                                'WIDTH {}\n'.format(len(points)),
                                'HEIGHT 1\n',
                                'VIEWPOINT 0 0 0 1 0 0 0\n',
                                'POINTS {}\n'.format(len(points)),
                                'DATA ascii\n']
        
                    with open(file_path, 'a') as f:
                        f.writelines(header)
                        for line in points:
                            f.writelines("{0} {1} {2} {3}\n".format(str(line[0]), str(line[1]), str(line[2]), str(int(line[3]))))
                    print("pcd saved done !!")

if __name__ == "__main__":
    print(cv2.__version__) 
    # image_topic = "/kitti/camera_gray_right/image_raw" 
    # point_topic = "/kitti/velo/pointcloud "   
    
    image_topic = "/rs/left_camera/compressed" # /usb_cam/image_raw/compressed
    point_topic = "/rslidar_points"   #"/percept_cloud_rviz"    #"/rslidar_points" 
    bagpath = "./test" # "/home/tangsonghe/work/data/rslidar/"
    bag2pcd_img(bagpath, image_topic, point_topic)
