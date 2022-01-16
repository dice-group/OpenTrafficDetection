## VEP Instructions

# Traffic Detection
Implementation in Python

# Cloning the repository
Clone the repo with:
```
git clone --recurse-submodules https://github.com/dice-group/VEP
```
If you already cloned and forgot to use ```--recurse-submodules``` you can run ```git submodule update --init```

# Configuring

Before run in the jetson board

check the wiki about how to install the SDK with:
https://github.com/dice-group/VEP/wiki/Configuring-the-Project-on-the-Jetson-TX2-Board

and install openCV for the jetson by executing install_opencv_jetson_tx2.sh

then, install PyTorch and Torch Vision for ARM CPUs:

PyTorch:
```
# install the dependencies (if not already onboard)
$ sudo apt-get install python3-pip libjpeg-dev libopenblas-dev libopenmpi-dev libomp-dev
$ sudo -H pip3 install future
$ sudo pip3 install -U --user wheel mock pillow
$ sudo -H pip3 install testresources
# upgrade setuptools 47.1.1 -> 58.3.0
$ sudo -H pip3 install --upgrade setuptools
$ sudo -H pip3 install Cython
# install gdown to download from Google drive
$ sudo -H pip3 install gdown
# download the wheel
$ gdown https://drive.google.com/uc?id=1TqC6_2cwqiYacjoLhLgrZoap6-sVL2sd
# install PyTorch 1.10.0
$ sudo -H pip3 install torch-1.10.0a0+git36449ea-cp36-cp36m-linux_aarch64.whl
# clean up
$ rm torch-1.10.0a0+git36449ea-cp36-cp36m-linux_aarch64.whl
```

TorchVision:
```
Used with PyTorch 1.10.0
# the dependencies
$ sudo apt-get install libjpeg-dev zlib1g-dev libpython3-dev
$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev
$ sudo pip3 install -U pillow
# install gdown to download from Google drive, if not done yet
$ sudo -H pip3 install gdown
# download TorchVision 0.11.0
$ gdown https://drive.google.com/uc?id=1C7y6VSIBkmL2RQnVy8xF9cAnrrpJiJ-K
# install TorchVision 0.11.0
$ sudo -H pip3 install torchvision-0.11.0a0+fa347eb-cp36-cp36m-linux_aarch64.whl
# clean up
$ rm torchvision-0.11.0a0+fa347eb-cp36-cp36m-linux_aarch64.whl
```

and finally, install the requirements with:

```
pip3 install -r requirements.txt
```

# Running the Application

To run with a video, use the command, replacing video.mp4 by your video file
```
python3 vep_yolov5.py --source video.mp4
```

To run with a camera installed, run :
```
python3 vep_yolov5.py --source camera
```

By default, the detections will be saved to `output_detection.txt`. To change the filename, use `--output <file_name.txt>`.

# Remote Server
You can send the detections to a remote server. Start the server with
```
python3 detections_server.py
```
Then run VEP with the command `--remote_server=<ip_address>:5005`

Always use the port 5005. It is the port that the server will listen. The machine host name, the timestamp and the detections will be sent in the message


# Training VEP Model

Download the VEP Dataset from:

```
https://hobbitdata.informatik.uni-leipzig.de/VEP/training_data/vep.tar.gz
```

and checkout the yolov5 repository and install the dependencies:

```
git clone https://github.com/ultralytics/yolov5
cd yolov5
pip install -r requirements.txt

```


Extract the vep.tar.gz file into the yolov5 folder and copy training/vep_l.yaml to yolov5/models.

Make sure that you have CUDA and CUDNN installed

inside the yolov5 folder, train the model with:
```
python3 train.py --img 448 --batch 224 --epochs 500 --data vep/vep.yaml --cfg models/vep_s.yaml --device 0
```

The device is the index of the GPU that you want to train. Switch to the fastest GPU available on your system.
If the GPU does not have enough memory, reduce the number of batches until you find one that fits the GPU memory.
When it is over, you can find the result in runs/train.

# VEP Training Results

For more detailed results, please check results/results.csv

# F1 Curve
![alt text](https://github.com/dice-group/VEP/blob/master/results/F1_curve.png)

# Precision-Recall Curve
![alt text](https://github.com/dice-group/VEP/blob/master/results/PR_curve.png)

# Precision Curve
![alt text](https://github.com/dice-group/VEP/blob/master/results/P_curve.png)

# Recall Curve
![alt text](https://github.com/dice-group/VEP/blob/master/results/R_curve.png)

# Confusion Matrix
![alt text](https://github.com/dice-group/VEP/blob/master/results/confusion_matrix.png)

