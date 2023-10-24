# coding=utf-8
from statistics import mode
import onnx
import os
import onnxruntime
import onnx_graphsurgeon as gs
import numpy as np
from onnxsim import simplify
import pdb

def main_load_model():
    # model_path = "superpoint_v4.onnx"
    model_path = "superpoint_v5.onnx"

    model = onnx.load(model_path)
    graphs = gs.import_onnx(model)
    nodes = model.graph.node
    tensors =  graphs.tensors()
    # print(graphs.input)
    print(graphs.outputs)
    print(len(nodes))
    # print((nodes))
    # print(nodes[12].op_type)
    # print(nodes[57].op_type)
    # for i in range(len(nodes)):
    #     if nodes[i].op_type == "ReduceL2":
    #         print("xxxx，",i)
    # pdb.set_trace()
    # graphs.nodes[45].op = "LpNormalization"
    # graphs.nodes[45].attrs = {"axis":1,"p":2}
    # model.graph.node[57].op_type = "lp_or"
    # print(model.graph.node[12].op_type)
    # print(model.graph.node[57].op_type)



    # print(nodes[26])
    # print(nodes[27])
    graphs.inputs = [tensors["input"]]
    graphs.outputs = [tensors["/relu_7/Relu_output_0"].to_variable(dtype=np.float32)]

    # graphs.outputs = [tensors["46"].to_variable(dtype=np.float32),tensors["49"].to_variable(dtype=np.float32)]
    # graphs.outputs = [tensors["46"],tensors["49"]]
    # graphs.outputs = [tensors["49"]]
    
    # remove_node = nodes[27]
    # nodes.remove(remove_node)
    # remove_node1 = nodes[26]
    # nodes.remove(remove_node1)
    graphs.cleanup()
    new_model = gs.export_onnx(graphs)
    onnx.checker.check_model(model)
    onnx.save(new_model,'out.onnx')
    # onnx.save(model,'out123.onnx')
    # graph.inputs=[]


if __name__ == '__main__':
    main_load_model()
