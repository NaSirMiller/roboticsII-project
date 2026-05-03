# roboticsII-project
## Exit Detection

Run `safe_exit_detection_node` node.

Run the following from the repo's root:

```bash
colcon build --packages-select exit_detection # rebuild package to recognize changes
source install/setup.bash # sync terminal to new package changes
ros2 launch exit_detection car_camera_proplus_bringup_launch.py # launch camera
ros2 launch exit_detection exit_detection_launch.py # launch color detection
```
## Robotics Utils

Shared utility that the other packages depend on. Must be built before packages that depend on it.

Run the following from the repo's root:

```bash
colcon build --packages-select robotics_utils # rebuild package to recognize changes
source install/setup.bash # sync terminal to new package changes
```