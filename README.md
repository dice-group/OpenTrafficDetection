## VEP Instructions

# Traffic Sensor
Implementation in Python

Before run, install the dependencies with

```
pip3 install python-magic
pip3 install numpy
```


# Running the Application

To run, clone the repository and access the python folder


```
git clone https://gitlab.opendata-paderborn.de/central/traffic_sensor/development
cd python
```

Now, you need to download the weights and the configuration for the darknet neural network.

```
wget https://pjreddie.com/media/files/yolov3.weights
wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg
```


Then, you can run the code with

```
python DetectObject.py <image_or_video_path>
```

<img src="https://i.ibb.co/fx42Pf7/Screenshot-from-2020-09-27-18-40-04.png" />

<img src="https://i.ibb.co/gwzwwZz/pic1.png" alt="pic1" border="0">

<img src="https://i.ibb.co/WtbbF8S/pic2.png" alt="pic2" border="0">



