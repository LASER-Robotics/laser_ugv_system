#!/bin/bash

curl -sSL http://get.gazebosim.org | sh

sudo apt -y install ros-noetic-gazebo-ros-pkgs

sudo apt-get install ros-noetic-teleop-twist-keyboard


cd ..

cd ..

sudo rosdep init

rosdep update

rosdep install -i --from-path src --rosdistro noetic -y

catkin build

