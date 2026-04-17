#!/usr/bin/env python3
"""
slam_launch.py

Launches slam_toolbox in online async mapping mode.

What slam_toolbox does:
  - Subscribes to /scan (LiDAR data from the robot)
  - Subscribes to /tf  (coordinate transforms: odom → base_footprint)
  - Publishes    /map  (OccupancyGrid, updated as the robot moves)
  - Publishes    /tf   (map → odom transform, so everything lines up)

Run with:
  ros2 launch slam_launch.py
  -- or --
  python3 slam_launch.py   (only works if ros2 launch infrastructure is available)
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    # ── Launch arguments (can be overridden on the command line) ──────────
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',           # set to 'true' when using Gazebo
        description='Use simulation clock'
    )

    use_sim_time = LaunchConfiguration('use_sim_time')

    # ── slam_toolbox parameters ────────────────────────────────────────────
    slam_params = {
        'use_sim_time': use_sim_time,

        # Coordinate frames — confirmed from Lab 3 (tracking_node.py uses base_footprint)
        'base_frame':  'base_footprint',  # Yahboom ROSMASTER X3 robot base frame
        'odom_frame':  'odom',            # wheel odometry frame
        'map_frame':   'map',             # the global map frame

        # LiDAR topic
        'scan_topic':  '/scan',       # change if your robot uses a different name

        # Map resolution and range
        'resolution':        0.05,    # meters per cell (5 cm)
        'max_laser_range':   10.0,    # meters — match your LiDAR spec

        # How often the map is saved to disk (seconds). 0 = never.
        'map_update_interval': 5.0,

        # Online async mode: builds map while robot moves, doesn't block navigation
        'mode': 'mapping',

        # Loop closure: detects when the robot revisits a place and corrects drift
        'do_loop_closing': True,
    }

    slam_node = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',   # "async" = non-blocking mode
        name='slam_toolbox',
        parameters=[slam_params],
        output='screen',
        remappings=[
            # If your robot publishes LiDAR on a different topic, remap here
            # ('/scan', '/robot/scan'),
        ]
    )

    return LaunchDescription([
        use_sim_time_arg,
        slam_node,
    ])
