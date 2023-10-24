
import onnx 
import numpy as np
import cv2
import os

import onnxruntime as ort



if __name__ == "__main__":

    print("*****")
    # file_path = "960_512_uint8_1.raw"
    file_path = "./local_data/test.raw"
    # file_path = "./data/960_512_float2.raw"
    # file_path = "./data/640_512_loc_uint8.raw"
    # file_path = "./data/1.raw"
    # file_path = "./data/1024_384_float.raw"
    # file_path = "./data/1664_480_float.raw"
    # file_path = "./data/960_416_float.raw"
    # file_path = "./data/det_seg.raw"

    # file_path = "704_384_float.raw"
    # file_path = "704_384_uint8.raw"

    # file_path = "1655868175-111326____.raw"

    with open(file_path, "rb") as f:
        binary_data = f.read()
    width = 640
    height = 512
    # width = 1024
    # height = 384
    # width = 1664
    # height = 480
    # width = 960
    # height = 416
    # width = 960
    # height = 512    
    # width = 1920
    # height = 864

    # image_data = np.frombuffer(binary_data, dtype=np.uint8).reshape(height, width, 3)
    # width = 704
    # height = 384
    # image_data = np.frombuffer(binary_data, dtype=np.uint8).reshape(height, width, 1)

    image_data = np.frombuffer(binary_data, dtype=np.float32).reshape(height, width, 1)
    # image_data = np.frombuffer(binary_data, dtype=np.uint8).reshape(height, width, 1)
    
    # print(np.max(image_data))
    # save_path = "./out.png"
    # cv2.imwrite(save_path, image_data)


    # onnx_path = "./det_pole_rm_ppp_modified.onnx"
    # onnx_path = "./det_pole_rm_0718_bbb_7.onnx"
    # onnx_path = "./out_8295.onnx"
    onnx_path = "./out.onnx"
    # onnx_path = "./superpoint_v5.onnx"
    # onnx_path = "./det_wide_dla3_8295.onnx"
    # onnx_path = "./0718_model/det_pole_rm3_8295.onnx"
    # onnx_path = "./seg_model/seg_qat_0823_split.onnx"
    # onnx_path = "./seg_model/seg.onnx"
    # onnx_path = "./narrow_model/det_narrow_crop.onnx"
    # onnx_path = "./seg_back/det_seg_back.onnx"
    # onnx_path = "./seg_model/seg_8295.onnx"
    # onnx_path = "./local/superpoint_v3.onnx"
    # onnx_path = "./0718_model/out.onnx"

    # onnx_path = "./det_wide_crop_0731_bbb_add.onnx"
    # onnx_path = "./0731_model/det_wide_crop_0731.onnx"
    # onnx_path = "./det_wide_crop_0731_8295_1_2.onnx"
    # onnx_path = "./det_pole_rm_0718_modified.onnx"
    # onnx_path = "./det_pole_rm_0718_fff_1.onnx"
    # onnx_path = "./det_wide_crop_0731_bbb.onnx"
    # onnx_path = "./resize_qat_modified.onnx"

    print("onnx_path is : ",onnx_path)
    
    sess = ort.InferenceSession(onnx_path,  providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])

    print(sess.get_inputs()[0].name)      

    input_name = sess.get_inputs()[0].name

    output_name= [output.name for output in sess.get_outputs()]
    print(output_name)

    print(image_data.shape)
    print(image_data[0][0])
    print(image_data[0][1])
    print(image_data[0][2])    
    print(image_data[0][3])
    print(image_data[0][4])
    print(image_data[0][5])

    # pixel_mean=[123.675, 116.280, 103.530]
    # pixel_std=[58.395, 57.120, 57.375]
    # image_data=(image_data-pixel_mean)/pixel_std
    print("max :", image_data.max())
    print("min :", image_data.min())


    image_data = image_data.transpose((2, 0, 1))
    print("input data shape ",image_data.shape)

    # print("input data",image_data[0][0])


    image_data = np.expand_dims(image_data, 0)

    print(image_data.shape)
    image_data = np.float32(image_data)
    # print(np.max(image_data))
    if 0:
        output = sess.run(output_name, {input_name:image_data})[0]
        
        print(output.shape)
        print(output.shape[0]*output.shape[1]*output.shape[2]*output.shape[3]*4)
        
        # 
        # B H W C
        output = output.transpose((1, 2, 0))
        # print(output[0][0][0][0:32])

        print(output.shape)

        # out_t = output[0][0][0][0]
        # # out_t = output[0][0][:][0] + 8.11506695e-10

        # print(out_t.shape)

        # for i in range(6):
        #     print(out_t[i*6:(i+1)*6])


        print("***********************")

        out_t = output[0][0][0]

        line_num = 11
        for i in range(line_num):
            print(out_t[i*6:(i+1)*6])
        print("-----------------------")
        
        out_t = output[0][0][1]

        for i in range(line_num):
            print(out_t[i*6:(i+1)*6])
        print("-----------------------")
        
        out_t = output[0][0][2]
        for i in range(line_num):
            print(out_t[i*6:(i+1)*6])
        print("-----------------------")
        
        out_t = output[0][0][3]
        for i in range(line_num):
            print(out_t[i*6:(i+1)*6])
        
        print("***********************")
    else:
        outputs = sess.run(output_name, {input_name:image_data})
        for o_i in range(len(outputs)):
            

            print("**********************************************************************************")
            # output = outputs[o_i]   #/0.07536981254816055
            output = outputs[o_i]
            print(output.shape)
            length = 4
            for s_i in range(len(output.shape)):
                length = length * output.shape[s_i]
            # print(output.shape[0]*output.shape[1]*output.shape[2]*output.shape[3]*4)
            print(length)
            print("onnx_path is : ",onnx_path)
            spec_name = os.path.basename(onnx_path)[:-5]
            print(spec_name)
            # print(output.shape[0]*output.shape[1]*output.shape[2]*output.shape[3]*4)
            # 
            # B H W C
            # if o_i==0:
            #     output = output.transpose((1, 2, 0))
            # else:
            #     output = output.transpose((0, 2, 3, 1))
            output = output.transpose((0, 2, 3, 1))
            # output = output.transpose((1, 2, 0))

            print(output.shape)

            
            # print(output[0][0][0][0:32])
            output_ = output.flatten()
            # output_.tofile("./{}_{}_onnx.result".format(spec_name, length))

            # print(output_.shape)
            num_line = 0
            for i in range(0, 64, 32):
                print(output_[i: i+32])
                num_line += 1
                if num_line % 6 == 0:
                    print("-------------------------------------------------")    
