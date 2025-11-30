#!/bin/bash
set -e

source /opt/ros/humble/setup.bash
source /ws/install/setup.bash

ros2 launch /ws/src/launch/project.launch.py

