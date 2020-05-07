image_name = 'D:/TDA4X_Learning/Team_work/000.jpeg'    #bgr
img = cv2.imread(image_name)
imgdata=img.reshape(3,1280,1920)

conv2_data = np.fromfile(file_path+'0003_00024_00320x00192.y', dtype=np.int8)
conv2_data = conv2_data.reshape(24, 192, 320)
conv2_data.tofile("conv2_data.bin")

filessss='RPNGEN.txt'
b = np.loadtxt(filessss, dtype=np.int8)
print(b.mean())
