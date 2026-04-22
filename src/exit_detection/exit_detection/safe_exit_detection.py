import struct
import cv2
import numpy as np
import rclpy
import yaml
from cv_bridge import CvBridge
from geometry_msgs.msg import PoseStamped
from message_filters import ApproximateTimeSynchronizer, Subscriber
from rclpy.node import Node
from sensor_msgs.msg import Image, PointCloud2
from tf2_ros import Buffer, TransformException, TransformListener
from robotics_utils.math import q2R

class SafeExitDetectionNode(Node):
    def __init__(self):
        super().__init__('safe_exit_detection_node')
        self.get_logger().info('Safe Exit Detection Node Started')
        self.declare_parameter('color_low', [60, 55, 50]) # Silver
        self.declare_parameter('color_high', [215, 205, 185])
        self.declare_parameter('object_size_min', 1000)
        self.br = CvBridge()
        self.tf_buffer = Buffer()
        self.goal_sent = False
        self.last_goal_time = self.get_clock().now()
        self.pose_saved = False
        self.save_path = '/root/yahboomcar_ros2_ws/yahboomcar_ws/src/exit_detection/saved_exit_pose.yaml'
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.pub_safe_exit = self.create_publisher(Image, '/detected_safe_exit', 10)
        self.pub_detected_safe_exit = self.create_publisher(PoseStamped, 'move_base_simple/goal', 10)
        self.sub_rgb = Subscriber(self, Image, '/camera/color/image_raw')
        self.sub_depth = Subscriber(self, PointCloud2, '/camera/depth/points')
        self.ts = ApproximateTimeSynchronizer([self.sub_rgb, self.sub_depth], 10, 0.1)
        self.ts.registerCallback(self.camera_callback)

    def camera_callback(self, rgb_msg, points_msg):
        self.get_logger().info('Received RGB and Depth Messages')
        param_color_low = np.array(self.get_parameter('color_low').value)
        param_color_high = np.array(self.get_parameter('color_high').value)
        param_object_size_min = self.get_parameter('object_size_min').value
        rgb_image = self.br.imgmsg_to_cv2(rgb_msg, "bgr8")
        hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2HSV)
        color_mask = cv2.inRange(hsv_image, param_color_low, param_color_high)
        contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            if w * h < param_object_size_min:
                return
            rgb_image = cv2.rectangle(rgb_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            center_x = int(x + w / 2)
            center_y = int(y + h / 2)
        else:
            return
        pointid = (center_y * points_msg.row_step) + (center_x * points_msg.point_step)
        (X, Y, Z) = struct.unpack_from('fff', points_msg.data, offset=pointid)
        center_points = np.array([X, Y, Z])
        if np.any(np.isnan(center_points)):
            return
        try:
            transform = self.tf_buffer.lookup_transform('map', rgb_msg.header.frame_id, rclpy.time.Time(), rclpy.duration.Duration(seconds=0.2))
            t_R = q2R(np.array([transform.transform.rotation.w, transform.transform.rotation.x, transform.transform.rotation.y, transform.transform.rotation.z]))
            cp_robot = t_R @ center_points + np.array([transform.transform.translation.x, transform.transform.translation.y, transform.transform.translation.z])
            detected_safe_exit_pose = PoseStamped()
            detected_safe_exit_pose.header.frame_id = 'map'
            detected_safe_exit_pose.header.stamp = rgb_msg.header.stamp
            detected_safe_exit_pose.pose.position.x = cp_robot[0]
            detected_safe_exit_pose.pose.position.y = cp_robot[1]
            detected_safe_exit_pose.pose.position.z = cp_robot[2]
            detected_safe_exit_pose.pose.orientation.w = 1.0
        except TransformException as e:
            self.get_logger().error('Transform Error: {}'.format(e))
            return

        now = self.get_clock().now()
        elapsed = (now - self.last_goal_time).nanoseconds / 1e9
        if not self.goal_sent or elapsed > 5.0:
            self.pub_detected_safe_exit.publish(detected_safe_exit_pose)
            self.last_goal_time = now
            self.goal_sent = True
            self.get_logger().info('Sent exit pose as nav goal')

        if not self.pose_saved:
            pose_data = {
                'x': detected_safe_exit_pose.pose.position.x,
                'y': detected_safe_exit_pose.pose.position.y,
                'z': detected_safe_exit_pose.pose.position.z,
                'qx': detected_safe_exit_pose.pose.orientation.x,
                'qy': detected_safe_exit_pose.pose.orientation.y,
                'qz': detected_safe_exit_pose.pose.orientation.z,
                'qw': detected_safe_exit_pose.pose.orientation.w,
            }
            with open(self.save_path, 'w') as f:
                yaml.dump(pose_data, f)
            self.pose_saved = True
            self.get_logger().info(f'Safe exit pose saved to {self.save_path}')

        detect_img_msg = self.br.cv2_to_imgmsg(rgb_image, encoding='bgr8')
        detect_img_msg.header = rgb_msg.header
        self.get_logger().info('image message published')
        self.pub_safe_exit.publish(detect_img_msg)

def main(args=None):
    rclpy.init(args=args)
    safe_exit_detection_node = SafeExitDetectionNode()
    rclpy.spin(safe_exit_detection_node)
    safe_exit_detection_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
