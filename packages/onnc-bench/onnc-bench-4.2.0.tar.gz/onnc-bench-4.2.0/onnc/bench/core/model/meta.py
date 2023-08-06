from typing import List
from pathlib import Path
from abc import abstractmethod
import shutil
from dataclasses import dataclass
import zipfile

from loguru import logger

from .transformer import ModelTransformer
from .model import Model, Tensor
from . import ModelFormat, ModelDataType
from .identifier import identify
from ..common import get_tmp_path
from importlib import import_module
import numpy as np


class MetadataRetriverRegistry(type):

    REGISTRY: List = []

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        if name != "MetadataRetriver":
            cls.REGISTRY.append(new_cls)
        return new_cls


class ModelMeta:

    def __init__(self, inputs: List[Tensor], outputs: List[Tensor]):
        self.inputs = inputs
        self.outputs = outputs


class MetadataRetriver(metaclass=MetadataRetriverRegistry):

    FORMAT: ModelFormat = ModelFormat.NON_SPECIFIED

    @classmethod
    def is_me(cls, model: Model) -> bool:
        return identify(model) == cls.FORMAT

    @abstractmethod
    def retrieve_inputs(self, model: Model) -> List[Tensor]:
        raise NotImplementedError("`retrieve_inputs` has to be implemented")

    @abstractmethod
    def retrieve_outputs(self, model: Model) -> List[Tensor]:
        raise NotImplementedError("`retrieve_outputs` has to be implemented")

    def retrieve(self, model: Model) -> ModelMeta:
        inputs = self.retrieve_inputs(model)
        logger.debug(f"Inputs of {model.name}: {inputs}")
        outputs = self.retrieve_outputs(model)
        logger.debug(f"Outputs of {model.name}: {outputs}")
        return ModelMeta(inputs=inputs, outputs=outputs)


def retrieve_model_metadata(model: Model) -> ModelMeta:
    for metadataretriever in MetadataRetriver.REGISTRY:
        if metadataretriever.is_me(model):
            return metadataretriever().retrieve(model)

    raise NotImplementedError(f"Unable to retrieve metadata of {model.format}")


class H5(MetadataRetriver):

    FORMAT = ModelFormat.H5

    from .dtype_map import TF_map

    def retrieve_inputs(self, model: Model) -> List[Tensor]:
        from tensorflow import keras  # type: ignore[import]
        _model = keras.models.load_model(model.src)

        res = []
        for x in _model.inputs:
            shape = tuple(-1 if not s else s for s in x.shape)
            res.append(
                Tensor(name=x.name, shape=shape,
                       dtype=self.TF_map.map(x.dtype)))
        return res

    def retrieve_outputs(self, model: Model) -> List[Tensor]:
        from tensorflow import keras  # type: ignore[import]
        _model = keras.models.load_model(model.src)

        res = []
        for x in _model.outputs:
            shape = tuple(-1 if not s else s for s in x.shape)
            res.append(
                Tensor(name=x.node.outbound_layer.name,
                       shape=shape,
                       dtype=self.TF_map.map(x.dtype)))

        return res


class ONNX(MetadataRetriver):

    FORMAT = ModelFormat.ONNX
    from .dtype_map import ONNX_map

    def retrieve_inputs(self, model: Model) -> List[Tensor]:
        import onnx
        onnx_model = onnx.load(model.src)

        input_all = [node.name for node in onnx_model.graph.input]
        input_initializer = [node.name for node in onnx_model.graph.initializer]
        net_feed_input = list(set(input_all) - set(input_initializer))

        res = []

        for input in onnx_model.graph.input:

            shape = tuple(
                xx.dim_value for xx in input.type.tensor_type.shape.dim)
            shape = tuple(-1 if int(s) == 0 else s for s in shape)

            if input.name in net_feed_input:
                res.append(
                    Tensor(input.name, shape,
                           self.ONNX_map.map(input.type.tensor_type.elem_type)))

        return res

    def retrieve_outputs(self, model: Model) -> List[Tensor]:
        import onnx
        model = onnx.load(model.src)
        res = []
        for model_output in model.graph.output:
            shape = tuple(
                s.dim_value for s in model_output.type.tensor_type.shape.dim)
            shape = tuple(-1 if int(s) == 0 else s for s in shape)
            res.append(
                Tensor(
                    model_output.name, shape,
                    self.ONNX_map.map(model_output.type.tensor_type.elem_type)))
        return res


class PTH(MetadataRetriver):

    FORMAT = ModelFormat.PTH
    from .dtype_map import NP_map

    def retrieve_inputs(self, model: Model) -> List[Tensor]:
        import torch
        _model = torch.load(model.src)
        tensor = list(_model.parameters())[  # type: ignore[union-attr]
            0].detach()
        t_name = "input" if tensor.name == None else tensor.name
        tensor = tensor.numpy()
        return [
            Tensor(t_name, tensor.shape, self.NP_map.map(tensor.dtype.type))
        ]

    def retrieve_outputs(self, model: Model) -> List[Tensor]:
        import torch
        _model = torch.load(model.src)

        # type: ignore[union-attr]
        tensor = list(_model.parameters())[-1].detach()
        t_name = "output" if tensor.name == None else tensor.name
        tensor = tensor.numpy()
        return [
            Tensor(t_name, tensor.shape, self.NP_map.map(tensor.dtype.type))
        ]


class PB(MetadataRetriver):

    FORMAT = ModelFormat.PB
    from .dtype_map import TF_map

    # https://stackoverflow.com/questions/43517959/given-a-tensor-flow-model-graph-how-to-find-the-input-node-and-output-node-name
    def _load_graph(self, frozen_graph_filename):
        import tensorflow as tf
        with tf.io.gfile.GFile(frozen_graph_filename, "rb") as f:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(f.read())
        with tf.Graph().as_default() as graph:
            tf.import_graph_def(graph_def)

        ops = graph.get_operations()
        return ops

    def retrieve_inputs(self, model: Model) -> List[Tensor]:
        import tensorflow as tf
        ops = self._load_graph(model.src)
        inputs = []
        for op in ops:
            if len(op.inputs) == 0 and op.type != 'Const':
                inputs.append(op)

        res = []
        """
        Eliminating "/" in the name is still under experiment
        This bug happens when converting bert-squad-384.pb which's input
        should be "logits" but is "import/logits" in the graph
        """
        for x in inputs:
            res.append(
                Tensor(name=x.name.split("/")[-1],
                       shape=tuple(xx if xx else -1 for xx in x.outputs[0].shape),
                       dtype=self.TF_map.map(x.outputs[0].dtype)))
        return res
        """
        >>> [x.size for x in graph_def.node[0].attr['shape'].shape.dim]
        [-1, 96, 96, 3]
        """

    def retrieve_outputs(self, model: Model) -> List[Tensor]:
        import tensorflow as tf
        ops = self._load_graph(model.src)
        inputs = []
        outputs_set = set(ops)

        for op in ops:
            if len(op.inputs) == 0 and op.type != 'Const':
                inputs.append(op)
            else:
                for input_tensor in op.inputs:
                    if input_tensor.op in outputs_set:
                        outputs_set.remove(input_tensor.op)

        outputs = list(outputs_set)
        res = []
        """
        Eliminating "/" in the name is still under experiment
        This bug happens when converting bert-squad-384.pb which's input
        should be "logits" but is "import/logits" in the graph
        """
        for x in outputs:
            res.append(
                Tensor(name=x.name.split("/")[-1],
                       shape=tuple(xx if xx else -1 for xx in x.outputs[0].shape),
                       dtype=self.TF_map.map(x.outputs[0].dtype)))
        return res


class SavedModel(MetadataRetriver):

    FORMAT = ModelFormat.SAVED_MODEL

    from .dtype_map import TF_map

    def retrieve_inputs(self, model: Model) -> List[Tensor]:
        assert type(model) == Model
        from tensorflow import keras  # type: ignore[import]
        _model = keras.models.load_model(model.src)
        return [
            Tensor(name=x.name,
                   shape=tuple(xx if xx else -1 for xx in x.shape),
                   dtype=self.TF_map.map(x.dtype)) for x in _model.inputs
        ]

    def retrieve_outputs(self, model: Model) -> List[Tensor]:

        from tensorflow import keras  # type: ignore[import]
        _model = keras.models.load_model(model.src)

        return [
            Tensor(name=x.name,
                   shape=tuple(xx if xx else -1
                               for xx in x.shape),
                   dtype=self.TF_map.map(x.dtype))
            for x in _model.inputs
            for x in _model.outputs
        ]


class ZippedSavedModel(SavedModel):

    FORMAT = ModelFormat.ZIPPED_SAVED_MODEL

    def retrieve_inputs(self, model: Model) -> List[Tensor]:
        temp = get_tmp_path()

        with zipfile.ZipFile(model.src,
                             'r') as zip_ref:  # type: ignore[arg-type]
            zip_ref.extractall(temp)
        return super().retrieve_inputs(Model(temp))

    def retrieve_outputs(self, model: Model) -> List[Tensor]:
        temp = get_tmp_path()
        with zipfile.ZipFile(model.src,
                             'r') as zip_ref:  # type: ignore[arg-type]
            zip_ref.extractall(temp)
        return super().retrieve_outputs(Model(temp))


class TFKerasModel(MetadataRetriver):

    FORMAT = ModelFormat.TF_KERAS_MODEL

    from .dtype_map import TF_map

    def retrieve_inputs(self, model: Model) -> List[Tensor]:
        return [
            Tensor(name=x.name,
                   shape=tuple(xx if xx else -1 for xx in x.shape),
                   dtype=self.TF_map.map(x.dtype)) for x in model.src.inputs
        ]

    def retrieve_outputs(self, model: Model) -> List[Tensor]:
        return [
            Tensor(name=x.name,
                   shape=tuple(xx if xx else -1 for xx in x.shape),
                   dtype=self.TF_map.map(x.dtype)) for x in model.src.outputs
        ]


class KerasModel(MetadataRetriver):
    '''
    Keras 2.5.0 Serializer
    '''

    FORMAT = ModelFormat.KERAS_MODEL
    from .dtype_map import TF_map

    def retrieve_inputs(self, model: Model) -> List[Tensor]:
        return [
            Tensor(name=x.name,
                   shape=tuple(xx if xx else -1 for xx in x.shape),
                   dtype=self.TF_map.map(x.dtype)) for x in model.src.inputs
        ]  # type: ignore[union-attr]

    def retrieve_outputs(self, model: Model) -> List[Tensor]:
        return [
            Tensor(name=x.name,
                   shape=tuple(xx if xx else -1 for xx in x.shape),
                   dtype=self.TF_map.map(x.dtype)) for x in model.src.outputs
        ]  # type: ignore[union-attr]


class PytorchModel(MetadataRetriver):
    """Use python MRO to check if it contains specific str"""

    FORMAT = ModelFormat.PT_NN_MODULE
    from .dtype_map import NP_map

    def retrieve_inputs(self, model: Model) -> List[Tensor]:
        _model = model.src
        tensor = list(_model.parameters())[  # type: ignore[union-attr]
            0].detach()
        t_name = "input" if tensor.name == None else tensor.name
        tensor = tensor.numpy()
        return [
            Tensor(t_name, tuple(x if x else -1 for x in tensor.shape),
                   self.NP_map.map(tensor.dtype.type))
        ]

    def retrieve_outputs(self, model: Model) -> List[Tensor]:
        _model = model.src

        # type: ignore[union-attr]
        tensor = list(_model.parameters())[-1].detach()
        t_name = "output" if tensor.name == None else tensor.name
        tensor = tensor.numpy()
        return [
            Tensor(t_name, tuple(x if x else -1 for x in tensor.shape),
                   self.NP_map.map(tensor.dtype.type))
        ]


class TorchTracedModel(MetadataRetriver):

    FORMAT = ModelFormat.TORCH_TRACED
    from .dtype_map import NP_map

    def retrieve_inputs(self, model: Model) -> List[Tensor]:
        import torch
        _model = torch.jit.load(model.src)
        tensor = list(_model.parameters())[  # type: ignore[union-attr]
            0].detach()
        t_name = "input" if tensor.name == None else tensor.name
        tensor = tensor.numpy()
        return [
            Tensor(t_name, tuple(x if x else -1 for x in tensor.shape),
                   self.NP_map.map(tensor.dtype.type))
        ]

    def retrieve_outputs(self, model: Model) -> List[Tensor]:
        import torch
        _model = torch.jit.load(model.src)

        # type: ignore[union-attr]
        tensor = list(_model.parameters())[-1].detach()
        t_name = "output" if tensor.name == None else tensor.name
        tensor = tensor.numpy()
        return [
            Tensor(t_name, tuple(x if x else -1 for x in tensor.shape),
                   self.NP_map.map(tensor.dtype.type))
        ]


class TFLiteModel(MetadataRetriver):
    """Use python MRO to check if it contains specific str"""

    FORMAT = ModelFormat.TFLITE
    from .dtype_map import NP_map
    _dtype_map = NP_map

    def retrieve_inputs(self, model: Model) -> List[Tensor]:

        try:
            import tflite_runtime.interpreter as tflite
            interpreter = tflite.Interpreter(model_path=str(model.src))
        except ModuleNotFoundError:
            import tensorflow as tf
            interpreter = tf.lite.Interpreter(model_path=str(model.src))

        res = []
        for i in interpreter.get_input_details():
            res.append(
                Tensor(i["name"],
                       tuple(-1 if not s else int(s) for s in i["shape"]),
                       self._dtype_map.map(i['dtype'])))
        return res

    def retrieve_outputs(self, model: Model) -> List[Tensor]:
        try:
            import tflite_runtime.interpreter as tflite
            interpreter = tflite.Interpreter(model_path=str(model.src))
        except ModuleNotFoundError:
            import tensorflow as tf
            interpreter = tf.lite.Interpreter(model_path=str(model.src))

        res = []
        for i in interpreter.get_output_details():
            res.append(
                Tensor(i["name"],
                       tuple(-1 if not s else int(s) for s in i["shape"]),
                       self._dtype_map.map(i['dtype'])))
        return res

class CaffeDir(MetadataRetriver):
    FORMAT = ModelFormat.CAFFE_DIR
    def retrieve_inputs(self, model: Model) -> List[Tensor]:
        return []
    def retrieve_outputs(self, model: Model) -> List[Tensor]:
        return []


class ZippedSavedModel(CaffeDir):

    FORMAT = ModelFormat.ZIPPED_CAFFE_DIR

    def retrieve_inputs(self, model: Model) -> List[Tensor]:
        temp = get_tmp_path()

        with zipfile.ZipFile(model.src,
                             'r') as zip_ref:  # type: ignore[arg-type]
            zip_ref.extractall(temp)
        return super().retrieve_inputs(Model(temp))

    def retrieve_outputs(self, model: Model) -> List[Tensor]:
        temp = get_tmp_path()
        with zipfile.ZipFile(model.src,
                             'r') as zip_ref:  # type: ignore[arg-type]
            zip_ref.extractall(temp)
        return super().retrieve_outputs(Model(temp))
