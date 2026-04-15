from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    config_dir = os.path.join(
        get_package_share_directory('path_generation'), 'config'
    )

    return LaunchDescription([
        Node(
            package='nav2_costmap_2d',
            executable='nav2_costmap_2d',
            name='global_costmap',
            parameters=[os.path.join(config_dir, 'costmap.yaml')],
            output='screen'
        ),
        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            parameters=[os.path.join(config_dir, 'path_planner.yaml')],
            output='screen'
        ),
        Node(
            package='path_generation',
            executable='path_generation_node',
            name='path_generation_node',
            output='screen'
        ),
    ])
