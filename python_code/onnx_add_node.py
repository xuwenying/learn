# coding=utf-8
import onnx
import os
import onnxruntime
import onnx_graphsurgeon as gs
import numpy as np
from onnxsim import simplify

def main_load_model():
    model_path = "det_pole_rm2.onnx"
    model = onnx.load(model_path)
    graphs = gs.import_onnx(model)
    nodes = model.graph.node
    tensors =  graphs.tensors()
    # print(graphs.input)
    print(graphs.outputs)
    print(len(nodes))
    print(nodes[25])
    print(nodes[26])
    print(nodes[27])
    graphs.inputs = [tensors["input"]]
    # graphs.outputs = [tensors["46"].to_variable(dtype=np.float32),tensors["49"].to_variable(dtype=np.float32)]
    # graphs.outputs = [tensors["46"],tensors["49"]]
    # graphs.outputs = [tensors["inputs"].to_variable(dtype=np.float32)]
    print("xxxxxxxxxxxxxxxxx")
    graphs.outputs.append(tensors["inputs.192"].to_variable(shape=[1, 13, 64, 120], dtype=np.float32))
    graphs.outputs.append(tensors["inputs.240"].to_variable(shape=[1, 13, 32, 60], dtype=np.float32))
    graphs.outputs.append(tensors["inputs.288"].to_variable(shape=[1, 13, 16, 30], dtype=np.float32))
    graphs.outputs.append(tensors["inputs.336"].to_variable(shape=[1, 13, 8, 15], dtype=np.float32))
    graphs.outputs.append(tensors["inputs.384"].to_variable(shape=[1, 13, 4, 8], dtype=np.float32))

    print(graphs.outputs)
    
    # remove_node = nodes[27]
    # nodes.remove(remove_node)
    # remove_node1 = nodes[26]
    # nodes.remove(remove_node1)
    graphs.cleanup()
    new_model = gs.export_onnx(graphs)
    onnx.checker.check_model(model)
    onnx.save(new_model,'out.onnx')
    # graph.inputs=[]


if __name__ == '__main__':
    main_load_model()
