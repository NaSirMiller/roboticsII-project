from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation clock'
    )
    use_sim_time = LaunchConfiguration('use_sim_time')

    launch_dir = os.path.join(
        get_package_share_directory('map_generation'), 'launch'
    )

    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_dir, 'slam_launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items(),
    )

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_dir, 'nav2_launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items(),
    )

    nav2_wfd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('nav2_wfd'),
                'launch',
                'wavefront_frontier_launch.py'
            )
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items(),
    )

    map_gen_node = Node(
        package='map_generation',
        executable='map_generation_node',
        name='map_generation',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
    )

    return LaunchDescription([
        use_sim_time_arg,
        slam,
        nav2,
        nav2_wfd,
        map_gen_node,
    ])
