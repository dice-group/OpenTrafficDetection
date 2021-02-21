## VEP Instructions

# Traffic Detection
Implementation in Python

Before run, install the dependencies with

```
pip3 install python-magic
pip3 install numpy
```


# Running the Application

To run, clone the repository and access the python folder


```
git clone https://github.com/dice-group/VEP
cd python
```

Now, you need to setup the models. Just run the **setup_models.sh** script

```
sh setup_models.sh
```


Then, you can run the program with:

```
python3 vep.py <image_or_video_path> <destination_file>
```

If you want to run using the system camera as input feed, run:

```
python3 vep.py camera <destination_file>
```





