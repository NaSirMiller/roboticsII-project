from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
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

    explore_lite = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_dir, 'explore_lite_launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items(),
    )

    return LaunchDescription([
        use_sim_time_arg,
        slam,
        nav2,
        explore_lite,
    ])
