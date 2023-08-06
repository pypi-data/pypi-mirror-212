# ONNC-bench

ONNC-bench is a Python wrapper of ONNC

## Installation

### Using pip

```
pip install onnc-bench
```

## Python API Example

Here is an example to show how to use ONNC python API

```
from onnc.bench import login, Project
# Setup your ONNC API key
api_key = "Your API KEY"
login(api_key)

# Instantiate a projct
project = Project('experiment-1')

# Add a model and its coresponding calibration samples
project.add_model('path/to/model', 'path/to/samples')

# Compile the model and optmize to `CMSIS-NN` backend
project.compile(target='CMSIS-NN-DEFAULT')


# Save the compiled model
deployment = project.save('./output')

```

Please Check https://docs-tinyonnc.skymizer.com/index.html for the full documents.
