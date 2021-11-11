## VEP Instructions

# Traffic Detection
Implementation in Python

Before run in the jetson board

check the wiki about how to install the SDK with:
https://github.com/dice-group/VEP/wiki/Configuring-the-Project-on-the-Jetson-TX2-Board

and install openCV for the jetson by executing install_opencv_jetson_tx2.sh

then, install the dependencies with

```
pip3 install -r requirements.txt
```

If you are instaling on Nvidia Jetson, please comment the pytorch dependency on the requirements file and install the version 1.8.0 following the instructions:
https://forums.developer.nvidia.com/t/pytorch-for-jetson-version-1-10-now-available/72048

or:

```
wget https://nvidia.box.com/shared/static/p57jwntv436lfrd78inwl7iml6p13fzh.whl -O torch-1.8.0-cp36-cp36m-linux_aarch64.whl
sudo apt-get install python3-pip libopenblas-base libopenmpi-dev 
pip3 install Cython
pip3 install numpy torch-1.8.0-cp36-cp36m-linux_aarch64.whl
```



# Running the Application

To run, clone the repository recursively:


```
git clone --recurse-submodules https://github.com/dice-group/VEP
```
If you already cloned and forgot to use ```--recurse-submodules``` you can run ```git submodule update --init```


# Training VEP

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

