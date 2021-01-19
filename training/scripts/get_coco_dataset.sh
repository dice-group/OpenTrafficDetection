#!/bin/bash

# Clone COCO API
git clone https://github.com/pdollar/coco
cd coco

mkdir images
cd images

# Download Images
#very slow downloading
#wget -c https://pjreddie.com/media/files/train2014.zip
#wget -c https://pjreddie.com/media/files/val2014.zip
wget -c http://images.cocodataset.org/zips/train2014.zip
wget -c http://images.cocodataset.org/zips/val2014.zip

# Unzip
unzip -q train2014.zip
unzip -q val2014.zip

cd ..

# Download COCO Metadata
wget -c https://pjreddie.com/media/files/instances_train-val2014.zip
wget -c https://pjreddie.com/media/files/coco/5k.part
wget -c https://pjreddie.com/media/files/coco/trainvalno5k.part
wget -c https://pjreddie.com/media/files/coco/labels.tgz
tar xzf labels.tgz
unzip -q instances_train-val2014.zip



