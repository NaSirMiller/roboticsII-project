#!/usr/bin/env python3
"""
explore_lite_launch.py

Launches explore_lite, which drives autonomous frontier exploration.

What explore_lite does:
  - Subscribes to /map           (occupancy grid from slam_toolbox)
  - Subscribes to /tf            (to know where the robot is)
  - Sends goals to Nav2 via      navigate_to_pose action
  - Publishes /explore/frontiers (MarkerArray — our node monitors this)

explore_lite finds the boundary between known-free and unknown cells
(frontiers), picks the nearest one, and sends it to Nav2 as a goal.
When Nav2 arrives, explore_lite picks the next frontier, and so on.
When no frontiers remain, it stops — our map_generation_node detects this.

Install (inside Docker on the robot):
  sudo apt install ros-humble-explore-lite
  -- or --
  sudo apt install ros-jazzy-explore-lite

Run with:
  ros2 launch explore_lite_launch.py
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation clock'
    )
    use_sim_time = LaunchConfiguration('use_sim_time')

    explore_node = Node(
        package='explore_lite',
        executable='explore',
        name='explore',
        parameters=[{
            'use_sim_time': use_sim_time,

            # Must match slam_toolbox and Nav2 frame settings
            'robot_base_frame': 'base_footprint',  # Yahboom ROSMASTER X3

            # How close to a frontier counts as "arrived" (meters)
            # Larger = less precise but fewer stuck situations
            'goal_blacklist_radius': 0.3,

            # Minimum size of a frontier to bother visiting (cells)
            # Filters out tiny gaps that aren't worth exploring
            'min_frontier_size': 0.25,

            # How often to re-evaluate which frontier to visit (seconds)
            # Lower = more responsive, higher = more stable
            'planner_frequency': 1.0,

            # Wait this long for Nav2 to accept a goal before giving up
            'progress_timeout': 30.0,

            # Visualise frontiers on /explore/frontiers topic
            # map_generation_node subscribes here to detect completion
            'visualize': True,
        }],
        output='screen',
    )

    return LaunchDescription([
        use_sim_time_arg,
        explore_node,
    ])
