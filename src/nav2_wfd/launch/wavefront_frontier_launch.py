from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='nav2_wfd',
            executable='explore',
            name='nav2_waypoint_tester',
            output='screen',
        ),
    ])
