# Video Streamer
This alwaysAI app performs realtime object detection and streams video and text data to a Flask-SocketIO server that can be located on another device.

## Setup
This app requires an alwaysAI account. Head to the [Sign up page](https://www.alwaysai.co/dashboard) if you don't have an account yet. Follow the instructions to install the alwaysAI toolchain on your development machine.

Next, create an empty project to be used with this app. When you clone this repo, you can run `aai app configure` within the repo directory and your new project will appear in the list.

## Usage
### Server
The server is a Flask-SocketIO server that hosts a webpage and a socketio server.

First, create the Python virtual environment with the dependencies. For example, on Linux run these steps:

```
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

Now, you should be able to run the app:

```
(venv) $ python app.py
[INFO] Starting server at http://localhost:5001
```

Open the link in a browser on your machine. Next, start the realtime object detection app.


### Realtime Object Detector
Once the alwaysAI toolset is installed on your development machine (or edge device if developing directly on it) you can run the following CLI commands:

To set up the target device & folder path

`$ aai app configure`

To install the app on the target device

`$ aai app install`

The app has the following options:

```
$ aai app start -- --help
usage: app.py [-h] [--camera CAMERA] [--use-streamer]
              [--server-addr SERVER_ADDR] [--stream-fps STREAM_FPS]

alwaysAI Video Streamer

optional arguments:
  -h, --help            show this help message and exit
  --camera CAMERA       The camera index to stream from.
  --use-streamer        Use the embedded streamer instead of connecting to the
                        server.
  --server-addr SERVER_ADDR
                        The IP address or hostname of the SocketIO server
                        (Default: localhost).
  --stream-fps STREAM_FPS
                        The rate to send frames to the server in frames per
                        second (Default: 20.0).
```

To start the app using the defaults:

`$ aai app start`

To capture video from camera index 1:

`$ aai app start -- --camera 1`

To connect to the server at 192.168.3.2:

`$ aai app start -- --server-addr 192.168.3.2`

To stream frames at 5 FPS:

`$ aai app start -- --stream-fps 5`

> Note that tha extra `--` in the above commands is used to indicate that the parameters that follow are to be passed through to the python app, rather than used by the CLI.

#### Example

Run the realtime object detector connecting to `192.168.3.2` and streaming at 5 FPS:

```
$ aai app start -- --server-addr 192.168.3.2 --stream-fps 5
Loaded model:
alwaysai/mobilenet_ssd

Engine: Engine.DNN
Accelerator: Accelerator.GPU

Labels:
['background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']

[INFO] Connecting to server http://192.168.3.2:5001...
[INFO] Successfully connected to server.
```
