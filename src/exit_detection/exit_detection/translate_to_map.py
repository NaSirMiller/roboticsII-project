import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, DurabilityPolicy
from geometry_msgs.msg import PoseStamped
import numpy as np
from tf2_ros import Buffer, TransformListener, TransformException
from robotics_utils.math import q2R


class TranslateToMapNode(Node):
    def __init__(self):
        super().__init__('translate_to_map_node')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.sub = self.create_subscription(PoseStamped, 'goal_pose_odom', self.pose_callback, 10)
        latched_qos = QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL)
        self.pub = self.create_publisher(PoseStamped, 'goal_pose', latched_qos)

    def pose_callback(self, pose_msg):
        try:
            transform = self.tf_buffer.lookup_transform(
                'map',
                pose_msg.header.frame_id,
                rclpy.time.Time(),
                rclpy.duration.Duration(seconds=0.2)
            )
            t = transform.transform.translation
            r = transform.transform.rotation
            R = q2R(np.array([r.w, r.x, r.y, r.z]))
            p = np.array([pose_msg.pose.position.x, pose_msg.pose.position.y, pose_msg.pose.position.z])
            p_map = R @ p + np.array([t.x, t.y, t.z])
            pose_in_map = PoseStamped()
            pose_in_map.header.frame_id = 'map'
            pose_in_map.header.stamp = pose_msg.header.stamp
            pose_in_map.pose.position.x = p_map[0]
            pose_in_map.pose.position.y = p_map[1]
            pose_in_map.pose.position.z = p_map[2]
            pose_in_map.pose.orientation.w = 1.0
            self.pub.publish(pose_in_map)
            self.get_logger().info(f'Stopping TranslateToMap node')
            # self.destroy_subscription(self.sub)  # stop receiving further messages

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