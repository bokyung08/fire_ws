#!/bin/bash
set -e

WS=~/fire_ws
SRC=$WS/src

mkdir -p $SRC
cd $SRC

echo "📦 fire_vision 생성"
ros2 pkg create fire_vision --build-type ament_python --dependencies rclpy std_msgs sensor_msgs cv_bridge

echo "📦 fire_distance 생성"
ros2 pkg create fire_distance --build-type ament_python --dependencies rclpy std_msgs geometry_msgs sensor_msgs nav_msgs

echo "📦 fire_slam 생성"
ros2 pkg create fire_slam --build-type ament_cmake --dependencies slam_toolbox nav_msgs

echo "📦 fire_bringup 생성"
ros2 pkg create fire_bringup --build-type ament_python --dependencies rclpy

mkdir -p fire_vision/launch fire_distance/launch fire_slam/launch fire_bringup/launch

echo "✅ fire_ws workspace 생성 완료"

