import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from tf2_ros import Buffer, TransformListener, TransformException
import tf2_geometry_msgs


class TranslateToMapNode(Node):
    def __init__(self):
        super().__init__('translate_to_map_node')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.sub = self.create_subscription(PoseStamped, 'goal_pose_odom', self.pose_callback, 10)
        self.pub = self.create_publisher(PoseStamped, 'goal_pose', 10)

    def pose_callback(self, pose_msg):
        try:
            transform = self.tf_buffer.lookup_transform(
                'map',
                pose_msg.header.frame_id,
                rclpy.time.Time(),
                rclpy.duration.Duration(seconds=0.2)
            )
            pose_in_map = tf2_geometry_msgs.do_transform_pose(pose_msg, transform)
            self.pub.publish(pose_in_map)
            self.get_logger().infp(f'Stopping TranslateToMap node')
            self.destroy_subscription(self.sub)  # stop receiving further messages

        except TransformException as e:
            self.get_logger().error(f'Transform Error: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = TranslateToMapNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()