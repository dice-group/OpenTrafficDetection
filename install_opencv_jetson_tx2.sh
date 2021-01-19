sudo apt-get -y purge *libopencv*
sudo apt-get -y update 
sudo apt-get -y upgrade 
pip3 install python-magic
sudo apt-get -y install build-essential cmake git unzip pkg-config libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libgtk2.0-dev libcanberra-gtk* python3-dev python3-numpy python3-pip libxvidcore-dev libx264-dev libgtk-3-dev libtbb2 libtbb-dev libdc1394-22-dev libv4l-dev v4l-utils libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libavresample-dev libvorbis-dev libxine2-dev libfaac-dev libmp3lame-dev libtheora-dev libopencore-amrnb-dev libopencore-amrwb-dev libopenblas-dev libatlas-base-dev libblas-dev liblapack-dev libeigen3-dev gfortran libhdf5-dev protobuf-compiler libprotobuf-dev libgoogle-glog-dev libgflags-dev
cd /usr/include/linux
sudo ln -s -f ../libv4l1-videodev.h videodev.h
cd ~/
echo 'Downloading pre configured opencv for TX2:'
wget https://hobbitdata.informatik.uni-leipzig.de/VEP/opencv.zip
wget https://hobbitdata.informatik.uni-leipzig.de/VEP/opencv_contrib.zip
unzip opencv.zip
unzip opencv_contrib.zip
rm opencv.zip
rm opencv_contrib.zip
cd opencv/build
echo 'Building openCV: '
make -j 2
sudo make install
cd ~/
rm -r opencv/
rm -r opencv_contrib/
