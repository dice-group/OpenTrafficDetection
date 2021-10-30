## VEP Instructions

# Traffic Detection
Implementation in Python

Before run, install the dependencies with

```
pip3 install -r requirements.txt
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
python3 train.py --img 448 --batch 16 --epochs 300 --data vep/vep.yaml --cfg models/vep_l.yaml --device 0
```

The device is the index of the GPU that you want to train. Switch to the fastest GPU available on your system.
If the GPU does not have enough memory, reduce the number of batches until you find one that fits the GPU memory.
When it is over, you can find the result in runs/train.

# VEP Training Results

For more detailed results, please check results/results.csv

![alt text](https://github.com/dice-group/VEP/blob/master/results/F1_curve.png)

![alt text](https://github.com/dice-group/VEP/blob/master/results/PR_curve.png)

![alt text](https://github.com/dice-group/VEP/blob/master/results/P_curve.png)

![alt text](https://github.com/dice-group/VEP/blob/master/results/R_curve.png)

![alt text](https://github.com/dice-group/VEP/blob/master/results/confusion_matrix.png)

