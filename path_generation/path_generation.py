from typing import Optional

from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import ComputePathToPose
from nav_msgs.msg import Path
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

class PathGenerationClientNode(Node):
  """
  Node acting as client for Nav2-SmacPlanner. 
  """
  def __init__(self) -> None:
    super().__init__("path_generation_node")
    self.get_logger().info('Path Generation Node Started')
    self._client = ActionClient(self, ComputePathToPose, 'compute_path_to_pose')
    self.path: Optional[Path] = None

  def request_path(self, goal_pose: PoseStamped) -> None:
        goal_msg = ComputePathToPose.Goal()
        goal_msg.goal = goal_pose
        goal_msg.planner_id = 'GridBased'
        future_goal_msg = self._client.send_goal_async(goal_msg)
        future_goal_msg.add_done_callback(self.goal_response_callback)  # called when server accepts/rejects

  def goal_response_callback(self, future) -> None:
    goal_handle = future.result()
    result_future = goal_handle.get_result_async()
    result_future.add_done_callback(self.result_callback)  # called when path is complete

  def result_callback(self, future):
    self.path = future.result().result.path  # nav_msgs/Path
    if self.path:
      self.get_logger().info("Path is generated, access via `.path`")
      

def main(args=None):
    rclpy.init(args=args)
    node = PathGenerationClientNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()