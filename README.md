# roboticsII-project

## Path Generation

### Overview

The Path Generation node interacts with Nav2's SmacPlanner, which implements a hybrid A* algorithm.

### Commands

Run the following from the repo's root:

```bash
colcon build --packages-select path_generation # rebuild package to recognize changes
source install/setup.bash # sync terminal to new package changes
ros2 launch path_generation planning.launch.py # launch and run node
```
