from pathlib import Path
from typing import Dict, Union, List
from pathlib import Path
import os
import json
import shutil

from loguru import logger
from onnc.bench.core.deployment import Deployment
from .builder import IBuilder
from onnc.bench.core.common import get_tmp_path
from . import Compilation
from onnc.bench.core.model.model import Model
from onnc.bench.core.dataset.dataset import Dataset


def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor


class NNUXEBuilder(IBuilder):
    BUILDER_NAME = "NNUXEBuilder"

    def __init__(self):
        self._compilations: Dict[int, Compilation] = {}
        self.output_path: str = ""

    def _compile(self,
                 model_name,
                 model_path: str,
                 sample_path: str,
                 params_path: str,
                 output_path: str,
                 local_nnuxe: bool = True):

        from nnuxe.drivers.compiler import compile as nnuxe_compile
        from nnuxe.core.report import CompileReport
        report = CompileReport()
        nnuxe_compile(model_path,
                      sample_path,
                      params_path,
                      os.path.join(output_path, model_name),
                      report,
                      local_nnuxe=local_nnuxe)
        return report

    def build(self, target: str, converter_params={}) -> Dict:

        compilation_list = []


        # Upload files and create compilation
        for iternal_cid in self._compilations:
            params = {}
            compilation = self._compilations[iternal_cid]
            params["target"] = target
            params["model_meta"] = compilation.model_meta
            params["sample_meta"] = compilation.sample_meta
            params["converter_params"] = converter_params
            compilation_list.append(
                (compilation.model_path, compilation.sample_path, params))
        output_path = get_tmp_path()
        os.makedirs(output_path, exist_ok=True)
        res = {}
        for idx, compi in enumerate(compilation_list):
            model_path = compi[0]
            sample_path = compi[1]
            params = compi[2]
            params_path = get_tmp_path()
            open(params_path, 'w').write(json.dumps(params))
            report = self._compile(f'model_{idx}', model_path, sample_path,
                                   params_path, output_path)
            res[f'model_{idx}'] = report
            report.dump_json(
                os.path.join(output_path, f'model_{idx}', "report.json"))

            os.remove(params_path)

            logger.debug(params)

        self.output_path = output_path

        return res

    def save(self, output: Path) -> Deployment:
        shutil.rmtree(output, ignore_errors=True)
        shutil.copytree(self.output_path, output)
        return Deployment(output)

    @property
    def supported_devices(self) -> Dict:
        devices = {
            'CMSIS-NN': 'CMSIS-NN',
            'ANDES-LIBNN': 'ANDES-LIBNN',
            'NVDLA-NV-SMALL': 'NVDLA-NV-SMALL',
            'NVDLA-NV-LARGE': 'NVDLA-NV-LARGE',
            'NVDLA-NV-FULL': 'NVDLA-NV-FULL',
            'CMSIS-NN-DEFAULT': 'CMSIS-NN-DEFAULT',
            'NVDLA-NV-SMALL-DEFAULT': 'NVDLA-NV-SMALL-DEFAULT',
            'NVDLA-NV-LARGE-DEFAULT': 'NVDLA-NV-LARGE-DEFAULT',
            'NVDLA-NV-FULL-DEFAULT': 'NVDLA-NV-FULL-DEFAULT',
            'NVIDIA-TENSORRT-FP32': 'NVIDIA-TENSORRT-FP32',
            'NVIDIA-TENSORRT-FP16': 'NVIDIA-TENSORRT-FP16',
            'NVIDIA-TENSORRT-INT8': 'NVIDIA-TENSORRT-INT8',
            'RELAYIR': 'RELAYIR',
            "INTEL-OPENVINO-CPU-FP32": "INTEL-OPENVINO-CPU-FP32",
            "FIXED_ONNX": "FIXED_ONNX",
            "ONNX": "ONNX",
            "ONNC-IN2O3": "ONNC-IN2O3",
            "GenericONNC": "GenericONNC"
        }
        return devices
