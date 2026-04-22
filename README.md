# roboticsII-project

## Path Generation

The Path Generation node interacts with Nav2's SmacPlanner, which implements a hybrid A* algorithm.

Run the following from the repo's root:

```bash
colcon build --packages-select path_generation # rebuild package to recognize changes
source install/setup.bash # sync terminal to new package changes
ros2 launch path_generation planning.launch.py # launch and run node
```

## Exit Detection

Runs three nodes: `danger_exit_detection_node`, `safe_exit_detection_node`, and `location_provider_node`.

Run the following from the repo's root:

```bash
colcon build --packages-select exit_detection # rebuild package to recognize changes
source install/setup.bash # sync terminal to new package changes
ros2 launch map_generation slam_launch.py
ros2 launch map_generation nav2_launch.py
ros2 launch map_generation explore_lite_launch.py
ros2 launch exit_detection exit_detection.launch.py # launch all three nodes
ros2 run map_generation map_generation_node
```

## Frontier Exploration

```shell
ros2 launch nav2_wfd wavefront_frontier.launch.py
```

## Robotics Utils

Shared utility that the other packages depend on. Must be built before packages that depend on it.

Run the following from the repo's root:

```bash
colcon build --packages-select robotics_utils # rebuild package to recognize changes
source install/setup.bash # sync terminal to new package changes
```

> src/nav2_wavefront_frontier_exploration/ is vendored from SeanReg/nav2_wavefront_frontier_exploration (commit 0747329), with modifications to use TF-based pose lookup instead of AMCL (see commit history for details).
