# coding=utf-8
import onnx
import os
import onnxruntime
import onnx_graphsurgeon as gs
import numpy as np
from onnxsim import simplify
from onnx import shape_inference

def main_load_model():
    model_path = "out2345.onnx"
    output_path = "out2345_size_11.onnx"
    onnx_model = onnx.load(model_path)  # load onnx model
    new_model = shape_inference.infer_shapes(onnx_model)
    model_simp, check = simplify(onnx_model)
    assert check, "Simplified ONNX model could not be validated"
    onnx.save(new_model, output_path)
    print('finished exporting onnx')


    # graph.inputs=[]


if __name__ == '__main__':
    main_load_model()
