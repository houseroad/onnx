# ATTENTION: The code in this file is highly EXPERIMENTAL.
# Adventurous users should note that the APIs will probably change.

"""onnx optimizer

This enables users to optimize their models.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import onnx
import onnx.onnx_cpp2py_export.optimizer as C  # type: ignore
from onnx import ModelProto

"""Apply the optimization on the serialized ModelProto.

Arguments:
    input (string or ModelProto): (serialized) model
    names (list of string): list of optimization names

Return:
    return (string or ModelProto depends on input) (serialized) optimized model

Supported pass names:
    -- nop
    -- eliminate_nop_transpose
    -- fuse_consecutive_transposes
    -- fuse_transpose_into_gemm
"""
def optimize(model, pass_list=None):
    if pass_list is None or len(pass_list) == 0:
        pass_list = ['eliminate_nop_transpose',
                     'fuse_consecutive_transposes',
                     'fuse_transpose_into_gemm']
    if not isinstance(model, ModelProto):
        raise ValueError('Optimizer only accepts ModelProto as first paramter, incorrect type: {}'.format(type(model)))

    model_str = model.SerializeToString()
    optimized_model_str = C.optimize(model_str, pass_list)
    return onnx.load_from_string(optimized_model_str)
