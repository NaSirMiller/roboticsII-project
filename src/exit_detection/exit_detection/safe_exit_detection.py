import struct
import cv2
import numpy as np
import rclpy
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
        self.br = CvBridge() # Used to convert between ROS and OpenCV images
        self.tf_buffer = Buffer()
        self.goal_sent = False
        self.last_goal_time = self.get_clock().now()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.pub_safe_exit = self.create_publisher(Image, '/detected_safe_exit', 10)
        self.pub_detected_safe_exit = self.create_publisher(PoseStamped, 'move_base_simple/goal', 10)
        self.sub_rgb = Subscriber(self, Image, '/camera/color/image_raw')
        self.sub_depth = Subscriber(self, PointCloud2, '/camera/depth/points')
        self.ts = ApproximateTimeSynchronizer([self.sub_rgb, self.sub_depth], 10, 0.1)
        self.ts.registerCallback(self.camera_callback)
        self.detected_exits = []

    def camera_callback(self, rgb_msg, points_msg):
        self.get_logger().info('Received RGB and Depth Messages') # Can comment out once know is working
        param_color_low = np.array(self.get_parameter('color_low').value)
        param_color_high = np.array(self.get_parameter('color_high').value)
        param_object_size_min = self.get_parameter('object_size_min').value
        rgb_image = self.br.imgmsg_to_cv2(rgb_msg,"bgr8")
        hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2HSV)
        color_mask = cv2.inRange(hsv_image, param_color_low, param_color_high)
        contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            if w * h < param_object_size_min:
                return
            rgb_image=cv2.rectangle(rgb_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            center_x = int(x + w / 2)
            center_y = int(y + h / 2)
        else:
            return
        pointid = (center_y*points_msg.row_step) + (center_x*points_msg.point_step)
        (X, Y, Z) = struct.unpack_from('fff', points_msg.data, offset=pointid)
        center_points = np.array([X,Y,Z])
        if np.any(np.isnan(center_points)):
            return
        try: # Transform center point from the camera frame to the world frame
            transform = self.tf_buffer.lookup_transform('map', rgb_msg.header.frame_id, rclpy.time.Time(), rclpy.duration.Duration(seconds=0.2))
            t_R = q2R(np.array([transform.transform.rotation.w, transform.transform.rotation.x, transform.transform.rotation.y, transform.transform.rotation.z]))
            cp_robot = t_R@center_points+np.array([transform.transform.translation.x, transform.transform.translation.y, transform.transform.translation.z])
            detected_safe_exit_pose = PoseStamped()
            detected_safe_exit_pose.header.frame_id = 'map'
            detected_safe_exit_pose.header.stamp = rgb_msg.header.stamp
            detected_safe_exit_pose.pose.position.x = cp_robot[0]
            detected_safe_exit_pose.pose.position.y = cp_robot[1]
            detected_safe_exit_pose.pose.position.z = cp_robot[2]
            detected_safe_exit_pose.pose.orientation.w = 1.0
            min_dist = 0.5 
            if not any(np.linalg.norm(cp_robot - p) < min_dist for p in self.detected_exits):
                self.detected_exits.append(cp_robot)
        except TransformException as e:
            self.get_logger().error('Transform Error: {}'.format(e))
            return

        now = self.get_clock().now()
        elapsed = (now - self.last_goal_time).nanoseconds / 1e9
        if not self.goal_sent or elapsed > 5.0:  # Only send every 5 seconds
            self.pub_detected_safe_exit.publish(detected_safe_exit_pose)
            self.last_goal_time = now
            self.goal_sent = True
            self.get_logger().info('Sent exit pose as nav goal')

        detect_img_msg = self.br.cv2_to_imgmsg(rgb_image, encoding='bgr8')
        detect_img_msg.header = rgb_msg.header
        self.get_logger().info('image message published') # NOTE: Can comment out once know is working
        self.pub_safe_exit.publish(detect_img_msg)

def main(args=None):
    rclpy.init(args=args)
    safe_exit_detection_node = SafeExitDetectionNode()
    rclpy.spin(safe_exit_detection_node)
    safe_exit_detection_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
