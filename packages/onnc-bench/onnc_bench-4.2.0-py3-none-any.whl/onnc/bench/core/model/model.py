from typing import Union, Tuple, Any, List, Type, Dict, Optional
from dataclasses import dataclass
from pathlib import Path
from collections import OrderedDict
from loguru import logger
from enum import Enum, auto

from . import ModelFormat, ModelDataType
from ..common import get_class_name


@dataclass
class Tensor:
    name: str
    shape: Union[None, Tuple[int, ...]] = None
    dtype: Union[None, ModelDataType] = None

    def dump(self) -> Dict:
        return {
            "name":
                self.name,
            "shape":
                self.shape,
            "type":
                self.dtype.name
                if isinstance(self.dtype, ModelDataType) else None
        }


class SrcType(Enum):
    OBJ = auto()
    FILE = auto()
    DIR = auto()


class Model():

    def __init__(self,
                 src: Union[str, Path, object],
                 format=ModelFormat.NON_SPECIFIED,
                 inputs: List[Union[List, Tuple, Tensor]] = None,
                 outputs: List[Union[List, Tuple, Tensor]] = None,
                 batch_dim=0):
        """
        Do not put identify_format in Model. Make sure
        (MVC) control and model are separated.
        """
        if not inputs:
            inputs = []
        if not outputs:
            outputs = []
        if isinstance(src, str):
            self.src = Path(src)
        else:
            self.src = src
        self.inputs: List[Tensor] = inputs
        self.outputs: List = outputs
        self.format = format
        self.batch_dim: int = batch_dim

        self._name: str
        if isinstance(src, str):
            self._name = Path(src).stem
        elif isinstance(src, Path):
            self._name = src.stem
        else:
            self._name = str(type(object))

    @property
    def name(self) -> str:
        return self._name

    def get_src_type(self) -> SrcType:
        """
          Return type of self.src
          Return None if self.src is not a valid path
        """

        if isinstance(self.src, str):
            path = Path(self.src)
        elif isinstance(self.src, Path):
            path = self.src
        else:
            return SrcType.OBJ

        if path.is_dir():
            return SrcType.DIR
        elif path.is_file():
            return SrcType.FILE
        else:
            return None

    def set_name(self, _name: str):
        self._name = _name

    def set_batch_dim(self, _batch_dim: Optional[int]):
        if _batch_dim is not None:
            assert _batch_dim >= 0
        self.batch_dim = _batch_dim

    def reset_inputs(self, input_: List[Tensor]) -> None:
        self.inputs = []
        for tensor in input_:
            self.inputs.append(tensor)

    def reset_outputs(self, output_: List[Tensor]) -> None:
        self.outputs = []
        for tensor in output_:
            self.outputs.append(tensor)

    def clone_attributes(self, model: Any) -> None:
        """Clone user defined attributes from input

        Iter all user-defined attributes and check if they have values.
        If the attribute of the destination object has value, then skip
        the clone.

        Args:
            model Type[Dataset]: The model object to be cloned
        """
        _to_be_cloned: List = []
        for attr_name in model.__dict__:

            dst_value = getattr(self, attr_name)
            src_value = getattr(model, attr_name)

            if (isinstance(dst_value, OrderedDict)) or (isinstance(
                    dst_value, List)):
                if len(dst_value) == 0:
                    _to_be_cloned.append([attr_name, src_value])

            elif dst_value is None:
                _to_be_cloned.append([attr_name, src_value])

        for attr_name, src_value in _to_be_cloned:
            setattr(self, attr_name, src_value)

    def dump(self) -> Dict:
        """
        WARNING: the dumped dictionary can only be used for report
        since src can be path or class name (which is not a good design)
        """
        data = {
            "src": "",
            "name": self.name,
            "inputs": {x.name: x.dump() for x in self.inputs},
            "outputs": {x.name: x.dump() for x in self.outputs},
            "format": self.format.name
        }
        if isinstance(self.src, str):
            data["src"] = self.src
        elif isinstance(self.src, Path):
            data["src"] = str(self.src)
        else:
            data["src"] = get_class_name(self.src)

        return data

    def load(self, obj: Dict):
        raise NotImplementedError()
