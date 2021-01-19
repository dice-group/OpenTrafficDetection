## VEP Instructions

#  Installing the environment on Jetson TX2 automatically.

To install all the Jetson dependencies, you gonna need a Host PC with ubuntu 18.04 or higher installed.
All the setup (Cuda, Cudnn and drivers) will be done automatically by the SDK manager.
You can download on the following link:
https://developer.nvidia.com/nvidia-sdk-manager
A Nvidia account is required. 

1 - Download the SDK Manager on the Host PC.

2 - If your ubuntu version is 20.04, open the file /etc/os-release and change the VERSION_ID to 18.04

3 - Make sure to start the Jetson on the recovery mode

4 - Start the Jetson board on Recovery mode. The board will light it up, but should not display video.
It should be pressed the two bottons as displayed on the image below:

<img src="https://gitlab.opendata-paderborn.de/central/traffic_sensor/development/-/raw/master/readme_files/start_board.jpg" /> 

5 - Plug the microusb cable on the board and connect into the Host PC. Start the SDK Manager. If everything was done right, it should
detect the board as described by the image below:

<img src="https://gitlab.opendata-paderborn.de/central/traffic_sensor/development/-/raw/master/readme_files/step01.png" /> 

6 - On Step 2, select all the components:

<img src="https://gitlab.opendata-paderborn.de/central/traffic_sensor/development/-/raw/master/readme_files/step02.png" /> 

7 - Proceed and wait for the installation to be finished. The board will boot up after the OS installation to configure the user
DO NOT CLOSE THE SDK MANAGER
The SDK manager will require a valid user and password from the OS installed on the board in order to install Cuda, Cudnn and additional drivers.

8 - After everything is finished, execute the **install_opencv_jetson_tx2.sh** to build opencv with Cuda and Cudnn for the TX2 board. 

9 - Install the camera drivers following the steps on https://github.com/alliedvision/linux_nvidia_jetson


# Traffic Sensor
Implementation in Python

Before run, install the dependencies with

```
pip3 install python-magic
pip3 install numpy
```

# Installing OpenCV Manually

The last dependency is OpenCV. 
You can install with pip
```
pip3 install opencv-python
```

However, this option won't have the GPU bindings, which will improve the performance significantly.
You need to download OpenCV source and compile it for your GPU.

The following tutorial is for the Ubuntu 20.04 OS.

## Install the dependencies

OpenCV uses intensively third-party software libraries. These must be installed on Ubuntu before OpenCV can be set up.
When they are already installed, no harm is done. This way, you are always sure you have the latest version.

```
sudo apt-get update
sudo apt-get upgrade
# install the dependencies
sudo apt-get install build-essential cmake git unzip pkg-config
sudo apt-get install libjpeg-dev libpng-dev libtiff-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install libgtk2.0-dev libcanberra-gtk*
sudo apt-get install python3-dev python3-numpy python3-pip
sudo apt-get install libxvidcore-dev libx264-dev libgtk-3-dev
sudo apt-get install libtbb2 libtbb-dev libdc1394-22-dev
sudo apt-get install libv4l-dev v4l-utils
sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
sudo apt-get install libavresample-dev libvorbis-dev libxine2-dev
sudo apt-get install libfaac-dev libmp3lame-dev libtheora-dev
sudo apt-get install libopencore-amrnb-dev libopencore-amrwb-dev
sudo apt-get install libopenblas-dev libatlas-base-dev libblas-dev
sudo apt-get install liblapack-dev libeigen3-dev gfortran
sudo apt-get install libhdf5-dev protobuf-compiler
sudo apt-get install libprotobuf-dev libgoogle-glog-dev libgflags-dev
# a symlink to videodev.h
cd /usr/include/linux
sudo ln -s -f ../libv4l1-videodev.h videodev.h
cd ~

```
## Download OpenCV.

When all third-party software is installed, OpenCV itself can be downloaded.
There are two packages needed; the basic version and the additional contributions.
Check before downloading the latest version at https://opencv.org/releases/.
If necessary, change the names of the zip files according to the latest version. After downloading, you can unzip the files.

```
cd ~
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.4.0.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.4.0.zip

unzip opencv.zip
unzip opencv_contrib.zip
```

The next step is some administration.
First, rename your directories with more convenient names like opencv and opencv_contrib.
This makes live later on easier. Next, make a directory where all the build files are located.

```
mv opencv-4.4.0 opencv
mv opencv_contrib-4.4.0 opencv_contrib

cd opencv
mkdir build
cd build
```

## Cuda
As known, the CUDA toolkit significantly improve the performance of deep learning software.
If you have an NVIDIA graphics card, you probably already have CUDA installed in the past.
If not, follow the instructions on Nvidia Site: https://developer.nvidia.com/cuda-downloads

## cuDNN

The NVIDIA CUDA Deep Neural Network library (cuDNN) is a GPU-accelerated library of primitives for deep neural networks.
cuDNN provides highly tuned implementations for standard routines such as forward and backward convolution, pooling, normalization, and activation layers.
cuDNN is part of the NVIDIA Deep Learning SDK.

To install cuDNN, go to https://developer.nvidia.com/cudnn (you need to create a nvidia account) and download the version based on the cuda installed on your system.
Then, unzip the cuDNN package
```
tar -xzvf cudnn-x.x-linux-x64-v8.x.x.x.tgz
```

Copy the following files into the CUDA Toolkit directory, and change the file permissions
```
sudo cp cuda/include/cudnn*.h /usr/local/cuda/include
sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn*.h /usr/local/cuda/lib64/libcudnn*
```


## Build Make

Go to the unzipped opencv folder and create a **build** folder

Here you tell CMake what, where and how to make OpenCV on your Ubuntu system.
There are many flags involved. The most you will recognize. We save memory by excluding any (Python) examples or tests.

To make it easy, you can build with cmake-gui
```
 sudo apt-get install cmake-qt-gui
```

Then run cmake (or cmake-gui) with the following options:

```
cmake -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
        -D BUILD_TIFF=ON \
        -D WITH_FFMPEG=ON \
        -D WITH_GSTREAMER=ON \
        -D WITH_TBB=ON \
        -D BUILD_TBB=ON \
        -D WITH_EIGEN=ON \
        -D WITH_V4L=ON \
        -D WITH_LIBV4L=ON \
        -D WITH_VTK=OFF \
        -D WITH_QT=OFF \
        -D WITH_OPENGL=ON \
        -D OPENCV_ENABLE_NONFREE=ON \
        -D INSTALL_C_EXAMPLES=OFF \
        -D INSTALL_PYTHON_EXAMPLES=OFF \
        -D BUILD_NEW_PYTHON_SUPPORT=ON \
        -D OPENCV_GENERATE_PKGCONFIG=ON \
        -D BUILD_TESTS=OFF \
        -D OPENCV_DNN_CUDA=ON \
        -D ENABLE_FAST_MATH=ON \
        -D CUDA_FAST_MATH=ON \
        -D CUDA_ARCH_BIN=7.5 \
        -D WITH_CUBLAS=ON \
        -D WITH_CUDNN=ON \
        -D CUDNN_LIBRARY=/usr/local/cuda/lib64/libcudnn.so.8.0.3 \
        -D CUDNN_INCLUDE_DIR=/usr/local/cuda/include  \ 
        -D BUILD_EXAMPLES=OFF ..
```

The **CUDA_ARCH_BIN** parameter refers to the compute capability of your GPU
you can consult the value for your GPU at https://developer.nvidia.com/cuda-gpus.

**CUDNN_LIBRARY** refers to the cuDNN lib that you installed. Be sure that you are referring the right file lib.

If everything went well, CMake comes with a report that looks something like the screenshot below.

<img src="https://qengineering.eu/images/Report-after-cmake.webp" alt="pic1" border="0">


## Make OpenCV

Now everything is ready for the build. This takes some time.
You can speed things up by using all your cores in your machine working simultaneously.
So take coffee and start building with the next command.
 
```
make -j <number_of_cpus_that_will_be_used>
```

Hopefully, your build was successful. Now to complete, install all the generated packages to the database of your system with the next commands.

```
sudo make install
sudo apt-get update

```

Now it is time to check your installation in Python 3.

<img src="https://qengineering.eu/images/OpenCV_4_4_0.webp" alt="pic1" border="0">

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



