from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='exit_detection',
            executable='navigate_to_saved_pose_node',
            name='navigate_to_saved_pose_node',
            output='screen'
        ),
    ])
