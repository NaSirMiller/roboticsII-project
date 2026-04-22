import rclpy
import yaml
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped

class NavigateToSavedPoseNode(Node):
    def __init__(self):
        super().__init__('navigate_to_saved_pose_node')
        self.save_path = '/root/yahboomcar_ros2_ws/yahboomcar_ws/src/exit_detection/saved_exit_pose.yaml'
        self.publisher = self.create_publisher(PoseStamped, 'move_base_simple/goal', 10)
        self.get_logger().info('Navigate To Saved Pose Node Started')
        self.get_logger().info('Waiting 3 seconds for Nav2 to be ready...')
        # Delay to ensure Nav2 is fully ready before sending goal
        self.timer = self.create_timer(3.0, self.send_goal)

    def send_goal(self):
        self.timer.cancel()  # Only send once

        try:
            with open(self.save_path, 'r') as f:
                pose_data = yaml.safe_load(f)
        except FileNotFoundError:
            self.get_logger().error(
                f'No saved pose found at {self.save_path}. '
                'Did the safe exit detection node run and detect an exit?'
            )
            return

        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.header.stamp = self.get_clock().now().to_msg()
        goal.pose.position.x = pose_data['x']
        goal.pose.position.y = pose_data['y']
        goal.pose.position.z = pose_data['z']
        goal.pose.orientation.x = pose_data['qx']
        goal.pose.orientation.y = pose_data['qy']
        goal.pose.orientation.z = pose_data['qz']
        goal.pose.orientation.w = pose_data['qw']

        self.publisher.publish(goal)
        self.get_logger().info(
            f'Sent saved exit pose as nav goal: '
            f'x={pose_data["x"]:.2f}, y={pose_data["y"]:.2f}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = NavigateToSavedPoseNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
