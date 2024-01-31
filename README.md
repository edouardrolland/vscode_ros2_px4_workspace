# ROS2 & PX4 VSCode Dev Envirnment  
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Build Status](https://github.com/edouardrolland/vscode_ros2_px4_workspace/actions/workflows/ros.yaml/badge.svg)](https://github.com/edouardrolland/vscode_ros2_px4_workspace/actions/workflows/ros.yaml)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

Welcome to our development environment template for ROS2, PX4, and Gazebo. This Docker-based setup enables seamless integration of ROS2, PX4, and Gazebo with VSCode, providing a robust environment for developing drone applications.

## Table of Contents

- [Introduction](#introduction)
- [Acknowledgment](#acknowledgment)
- [Features](#features)
- [How to Use the Template](#how-to-use-the-template)
  - [Prerequisites](#prerequisites)
  - [Getting Started](#getting-started)
- [License](#license)


## Acknowledgment

This template extends the [vscode_ros2_workspace](https://github.com/athackst/vscode_ros2_workspace#readme) template by incorporating the PX4-Autopilot library as well as simulations in Gazebo. For more information about the original template, please visit the [author's website](https://www.allisonthackston.com/articles/vscode-docker-ros2.html).

## Features

- ROS2 Integration
- PX4 Integration and Micro XRCE-DDS Agent & Client Setup
- Gazebo Simulation
- VSCode Workflow

## How to Use the Template

### Prerequisites

Before using this template, make sure you have the following prerequisites installed on your system:

- [Docker](https://docs.docker.com/engine/install/)
- [VSCode](https://code.visualstudio.com/)
- [VSCode Remote Containers Plugin](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Getting Started

#### Step 1: Get the Template

![Step 1](https://github.com/edouard98/vscode_ros2_px4_workspace/blob/humble/asset/1.png)

#### Step 2: Create Your Own Project Repository

![Step 2](https://github.com/edouard98/vscode_ros2_px4_workspace/blob/humble/asset/2.png)

#### Step 3: Clone the Project to Your Computer

![Step 3](https://github.com/edouard98/vscode_ros2_px4_workspace/blob/humble/asset/3.png)

#### Step 4: Open the Folder in VSCode

To interact with the container, you need to install the Docker extension in VSCode. Follow the steps below:

![Step 4](https://github.com/edouard98/vscode_ros2_px4_workspace/blob/humble/asset/4.png)

#### Step 5: Build the Container

You can build the container for the first time by following the steps presented in the following picture.

![Step 5](https://github.com/edouard98/vscode_ros2_px4_workspace/blob/humble/asset/5.png)

Please note that if you're on Windows, ensure that Docker Engine is running in the background. The initial build may take some time.

## Test your container
 
To test your contrainer and also the Gazebo installation you can run the following commands in the terminal.  

```
cd
cd PX4-Autopilot/
make px4_sitl gz_x500
```

This set of commands should open a Gazebo Tab display a drone as presented in the following figure. If the command is not displaying a tab, you should refer to the FAQ section of this readme to set up a X server. 

![Step 6](https://github.com/edouard98/vscode_ros2_px4_workspace/blob/humble/asset/6.png)

## FAQ

### WSL2

#### The gui doesn't show up

This is likely because the DISPLAY environment variable is not getting set properly.

1. Find out what your DISPLAY variable should be

      In your WSL2 Ubuntu instance

      ```
      echo $DISPLAY
      ```

2. Copy that value into the `.devcontainer/devcontainer.json` file

      ```jsonc
      	"containerEnv": {
		      "DISPLAY": ":0",
         }
      ```

#### I want to use vGPU

If you want to access the vGPU through WSL2, you'll need to add additional components to the `.devcontainer/devcontainer.json` file in accordance to [these directions](https://github.com/microsoft/wslg/blob/main/samples/container/Containers.md)

```jsonc
	"runArgs": [
		"--network=host",
		"--cap-add=SYS_PTRACE",
		"--security-opt=seccomp:unconfined",
		"--security-opt=apparmor:unconfined",
		"--volume=/tmp/.X11-unix:/tmp/.X11-unix",
		"--volume=/mnt/wslg:/mnt/wslg",
		"--volume=/usr/lib/wsl:/usr/lib/wsl",
		"--device=/dev/dxg",
      		"--gpus=all"
	],
	"containerEnv": {
		"DISPLAY": "${localEnv:DISPLAY}", // Needed for GUI try ":0" for windows
		"WAYLAND_DISPLAY": "${localEnv:WAYLAND_DISPLAY}",
		"XDG_RUNTIME_DIR": "${localEnv:XDG_RUNTIME_DIR}",
		"PULSE_SERVER": "${localEnv:PULSE_SERVER}",
		"LD_LIBRARY_PATH": "/usr/lib/wsl/lib",
		"LIBGL_ALWAYS_SOFTWARE": "1" // Needed for software rendering of opengl
	},
```

### Repos are not showing up in VS Code source control

This is likely because vscode doesn't necessarily know about other repositories unless you've added them directly. 

```
File->Add Folder To Workspace
```

![Screenshot-26](https://github.com/athackst/vscode_ros2_workspace/assets/6098197/d8711320-2c16-463b-9d67-5bd9314acc7f)


Or you've added them as a git submodule.

![Screenshot-27](https://github.com/athackst/vscode_ros2_workspace/assets/6098197/8ebc9aac-9d70-4b53-aa52-9b5b108dc935)

To add all of the repos in your *.repos file, run the script

```bash
python3 .devcontainer/repos_to_submodules.py
```

or run the task titled `add submodules from .repos`
