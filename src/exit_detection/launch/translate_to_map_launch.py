from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='exit_detection',
            executable='translate_to_map_node',
            name='translate_to_map_node',
            output='screen'
        ),
    ])
