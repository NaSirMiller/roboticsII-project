from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='exit_detection',
            executable='location_provider_node',
            name='location_provider_node',
            output='screen'
        ),
    ])
