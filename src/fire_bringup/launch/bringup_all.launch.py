from launch import LaunchDescription
from launch_ros.actions import Node, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    return LaunchDescription([

        # 🔥 화재 인식 + 시리얼
        Node(package='fire_vision', executable='fire_detector_onnx'),
        Node(package='fire_vision', executable='fire_serial_sender'),

        # 🎯 거리 측정 파이프라인 (네 구현)
        Node(package='fire_distance', executable='fire_centering_node'),
        Node(package='fire_distance', executable='fire_rotation_measure_node'),
        Node(package='fire_distance', executable='fire_distance_controller_node'),

        # 🗺 SLAM
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory('fire_slam'),
                    'launch/slam.launch.py'
                )
            )
        )
    ])
