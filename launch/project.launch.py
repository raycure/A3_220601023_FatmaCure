from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='sensor_publisher_pkg',
            executable='sensor_publisher'
        ),
        Node(
            package='data_processor_pkg',
            executable='data_processor'
        ),
        Node(
            package='command_server_pkg',
            executable='command_server'
        ),
    ])
