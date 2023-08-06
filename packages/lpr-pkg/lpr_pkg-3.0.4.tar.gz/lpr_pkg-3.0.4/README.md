# Introduction 
This repo serves as a Model release template repo. This includes everything from onnx conversion up to model release into production with all nessasry configs.

# Getting Started
To get started you need to fork this repo, and start going through it and fitting it to your use case as described below.
1.	[Makefile](#1-makefile)
2.	[Dependency management](#2-dependency-management)
3.  Configs
4.	Package code
5.	Onnx conversion
6.  Trt conversion
7.  Handlers
8.  Testing
9.  Flask app

# 1. Makefile
The makefile is the interface where developers interact with to perform any task. Below is the description of each command:
- download-saved-model: Download artifacts stored on mlflow at a certain epoch. Make sure to fill configs/config.yaml

- download-registered-model: Pull artifacts from model registry. Pass DEST as directory to store in. Make sure to fill configs/config.yaml

- convert-to-onnx: Run convert to onnx script.

- convert-trt: build & run container that performs trt 
conversion and yeild to artifacts/trt_converted. Pass FP(floating point) BS(batch size) DEVICE(gpu device) ONNX_PATH(path to onnx weights)
- trt-exec: command to be executed from inside the trt container, perform the conversion and copies the model to outside container

- predict-onnx: predict using onnx weights. Pass DATA_DIR(directory of data to be predicted) ONNX_PATH(path to onnx weights) CONFIG_PATH(Model config path) OUTPUT(output path directory)

- predict-triton: predict by sending to a hosted triton server. Pass DATA_DIR(directory of data to be predicted) IP(ip of server) PORT(port of triton server) MODEL_NAME(model name on triton) CONFIG_PATH(Model config path) OUTPUT(output path directory)

- evaluate: evaluate predicted results and write out metrics. Pass MODEL_PREDS(model predictions directory) GT(ground truth directory) OUTPUT(output path)

- python-unittest: Run python tests defined.

- bash-unittest: Run defined bash tests.

- quick-host-onnx: setup triton folder structure by copying nessasarry files, then hosting a triton server container. Pass ONNX_PATH

- quick-host-trt: setup triton folder structure by copying nessasarry files, then hosting a triton server container. Pass FP(floating point) BS(batch size) DEVICE(gpu device)

- host-endpoint: preform quick-host-trt and build and start flask container. Pass FP(floating point) BS(batch size) DEVICE(gpu device)

- setup-flask-app: command to be executed from inside the flask container.

- push-model: push model to Model registry.

- build-publish-pypi: build package folder into a pypi package and push the package to registry. 



# 2. Dependency Management
