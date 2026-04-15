from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='exit_detection',
            executable='safe_exit_detection_node',
            name='safe_exit_detection_node',
            output='screen'
        ),
    ])
