#!/bin/bash

curl -sSL http://get.gazebosim.org | sh

sudo apt -y install ros-humble-gazebo-ros-pkgs

sudo apt -y install ros-humble-ros2-control ros-humble-ros2-controllers ros-humble-gazebo-ros2-control

echo "source /usr/share/gazebo/setup.sh" >> ~/.bashrc

echo "export ROS_LOCALHOST_ONLY=1" >> ~/.bashrc

cd ..

cd ..

sudo rosdep init

rosdep update

rosdep install -i --from-path src --rosdistro humble -y

colcon build


