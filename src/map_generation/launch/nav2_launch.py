#!/usr/bin/env python3
"""
nav2_launch.py

Launches the Nav2 navigation stack.

What Nav2 does:
  - Subscribes to /map          (the occupancy grid from slam_toolbox)
  - Subscribes to /odom         (odometry from the robot)
  - Subscribes to /scan         (LiDAR, for obstacle avoidance)
  - Subscribes to /tf           (coordinate transforms)
  - Accepts action  navigate_to_pose  (our orchestrator sends goals here)
  - Publishes  /cmd_vel         (velocity commands to drive the robot)

Nav2 internal pipeline for a single goal:
  navigate_to_pose (action)
    → BT Navigator  (behaviour tree: plan, execute, recover on failure)
      → Global Planner  (finds a path on the full map using A*/Dijkstra)
      → Local Controller  (follows the path, avoids real-time obstacles)
        → /cmd_vel  (sent to the robot's motor driver)

Run with:
  ros2 launch nav2_launch.py
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    # ── Launch arguments ──────────────────────────────────────────────────
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation clock'
    )
    use_sim_time = LaunchConfiguration('use_sim_time')

    # ── Shared Nav2 parameters ────────────────────────────────────────────
    # These are passed to every Nav2 node.
    nav2_params = {
        'use_sim_time': use_sim_time,
    }

    # ── 1. Map Server ──────────────────────────────────────────────────────
    # Normally used to load a pre-saved map.
    # Since we're doing live SLAM, slam_toolbox already publishes /map,
    # so the map_server is NOT needed here — we just use the live /map.

    # ── 2. AMCL (localisation) ────────────────────────────────────────────
    # Normally used when you have a pre-built map.
    # Since slam_toolbox handles localisation (it publishes map→odom TF),
    # AMCL is NOT needed here either.

    # ── 3. Planner server ─────────────────────────────────────────────────
    # Finds a collision-free path from current pose to goal on /map.
    planner_server = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        parameters=[nav2_params, {
            'planner_plugins': ['GridBased'],
            'GridBased': {
                'plugin': 'nav2_navfn_planner/NavfnPlanner',  # Dijkstra-based
                'tolerance': 0.5,       # meters — how close to goal is "close enough"
                'use_astar': True,      # True = A*, False = Dijkstra
                'allow_unknown': True,  # allow planning through unexplored cells
            },
            'global_costmap': {
                'robot_base_frame': 'base_footprint',  # Yahboom ROSMASTER X3
            },
        }],
        output='screen',
    )

    # ── 4. Controller server ───────────────────────────────────────────────
    # Executes the path in real-time, handles local obstacle avoidance.
    controller_server = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        parameters=[nav2_params, {
            'controller_plugins': ['FollowPath'],
            'FollowPath': {
                'plugin': 'dwb_core::DWBLocalPlanner',  # Dynamic Window Approach
                # Speed limits confirmed from Lab 3 tracking_node.py:
                # linear clipped to ±0.3 m/s, angular to ±1.5 rad/s
                'min_vel_x':     0.0,
                'max_vel_x':     0.25,   # m/s — slightly under 0.3 for safety margin
                'max_vel_theta': 1.5,    # rad/s
                'min_speed_xy':  0.0,
                'max_speed_xy':  0.25,
                'base_frame_id': 'base_footprint',   # Yahboom ROSMASTER X3
            },
            'local_costmap': {
                'robot_base_frame': 'base_footprint',  # Yahboom ROSMASTER X3
            },
        }],
        output='screen',
    )

    # ── 5. Behaviour Tree Navigator ────────────────────────────────────────
    # Orchestrates the navigate_to_pose action:
    # plan → control → recover if stuck → re-plan as needed
    bt_navigator = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        parameters=[nav2_params, {
            'global_frame':       'map',
            'robot_base_frame':   'base_footprint',  # Yahboom ROSMASTER X3
            'odom_topic':         '/odom',
            'default_nav_to_pose_bt_xml': '/opt/ros/foxy/share/nav2_bt_navigator/behavior_trees/navigate_w_replanning_and_recovery.xml',
            # Only load plugins actually used by the BT XML above.
            # The default list includes nav2_change_goal_node_bt_node which
            # is not installed on this system and causes a fatal startup crash.
            'plugin_lib_names': [
                'nav2_compute_path_to_pose_action_bt_node',   # ComputePathToPose
                'nav2_follow_path_action_bt_node',            # FollowPath
                'nav2_clear_costmap_service_bt_node',         # ClearEntireCostmap
                'nav2_goal_updated_condition_bt_node',        # GoalUpdated
                'nav2_spin_action_bt_node',                   # Spin
                'nav2_wait_action_bt_node',                   # Wait
                'nav2_rate_controller_bt_node',               # RateController
                'nav2_recovery_node_bt_node',                 # RecoveryNode
                'nav2_pipeline_sequence_bt_node',             # PipelineSequence
            ],
        }],
        output='screen',
    )

    # ── 6. Lifecycle manager ───────────────────────────────────────────────
    # Nav2 nodes use a "lifecycle" pattern — they must be explicitly
    # activated before they start working. This manager does that automatically.
    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        parameters=[nav2_params, {
            'autostart': True,   # activate all nodes automatically on launch
            'node_names': [
                'planner_server',
                'controller_server',
                'bt_navigator',
            ]
        }],
        output='screen',
    )

    return LaunchDescription([
        use_sim_time_arg,
        planner_server,
        controller_server,
        bt_navigator,
        lifecycle_manager,
    ])
