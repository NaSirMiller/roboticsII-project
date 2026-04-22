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

    return LaunchDescription([
        use_sim_time_arg,
        Node(
            package='nav2_wfd_tf',
            executable='explore',
            name='wavefront_frontier_explorer',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
        ),
    ])
