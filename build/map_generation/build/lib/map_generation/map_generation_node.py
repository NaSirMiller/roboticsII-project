#!/usr/bin/env python3
"""
map_generation_node.py 

Orchestrates autonomous building exploration:

  slam_toolbox  →  builds occupancy grid on /map
  nav2_wfd      →  picks frontier waypoints, sends to Nav2
  Nav2          →  drives robot to each waypoint

Flow
----
  1. Record home pose from TF at startup
  2. Let nav2_wfd + Nav2 run until no frontiers remain
  3. Navigate back to home pose via Nav2 action
  4. Publish status="done" so Na'Sir's PathGeneration can start

Interfaces 
-----------------------------------------
PUBLISHES:
  /map_generation/status    std_msgs/String
      "exploring"  →  "returning_home"  →  "done"

  /map_generation/home_pose  geometry_msgs/PoseStamped
      Robot's starting position in the map frame.
      Published on startup and again when home is reached.

  /map                       nav_msgs/OccupancyGrid
      Published automatically by slam_toolbox (not this node).
      PathGeneration should use this after status == "done".

SUBSCRIBES:
  /explore/done              std_msgs/Bool
      Published by nav2_wfd when no frontiers remain.
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.duration import Duration

from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String, Bool
from nav2_msgs.action import NavigateToPose

import tf2_ros


class MapGenerationNode(Node):

    def __init__(self):
        super().__init__('map_generation')

        # ── Internal state ─────────────────────────────────────────────────
        self.home_pose: PoseStamped | None = None
        self.exploration_done = False

        # ── TF (to read robot position) ────────────────────────────────────
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # ── Nav2 action client ─────────────────────────────────────────────
        self._nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # ── Publishers ─────────────────────────────────────────────────────
        self._status_pub = self.create_publisher(
            String, '/map_generation/status', 10)
        self._home_pub = self.create_publisher(
            PoseStamped, '/map_generation/home_pose', 10)

        # ── Subscribers ────────────────────────────────────────────────────
        self.create_subscription(
            Bool,
            '/explore/done',
            self._explore_done_callback,
            1
        )

        # ── Timers ─────────────────────────────────────────────────────────
        # Try to record home pose a couple seconds after startup
        # (TF tree may not be ready immediately at t=0)
        self.create_timer(2.0, self._record_home_pose_once)

        self._publish_status('exploring')
        self.get_logger().info('MapGenerationNode started – waiting for nav2_wfd.')

    # ──────────────────────────── callbacks ───────────────────────────────

    def _explore_done_callback(self, msg: Bool):
        """
        Called when nav2_wfd publishes /explore/done.
        Signals that all frontiers have been explored.
        """
        if msg.data and not self.exploration_done:
            self.get_logger().info('nav2_wfd reported no more frontiers → exploration complete.')
            self.exploration_done = True
            self._return_home()

    def _record_home_pose_once(self):
        """
        Look up the robot's current position in the map frame and store it
        as home_pose. Retries every 2 s until it succeeds.
        """
        if self.home_pose is not None:
            return  # already done

        try:
            tf = self.tf_buffer.lookup_transform(
                'map',             # target frame
                'base_footprint',  # Yahboom ROSMASTER X3 robot base frame
                rclpy.time.Time(),
                timeout=Duration(seconds=1.0)
            )
            pose = PoseStamped()
            pose.header.stamp = self.get_clock().now().to_msg()
            pose.header.frame_id = 'map'
            pose.pose.position.x = tf.transform.translation.x
            pose.pose.position.y = tf.transform.translation.y
            pose.pose.position.z = tf.transform.translation.z
            pose.pose.orientation  = tf.transform.rotation

            self.home_pose = pose
            self._home_pub.publish(self.home_pose)
            self.get_logger().info(
                f'Home pose recorded: '
                f'x={pose.pose.position.x:.2f}  y={pose.pose.position.y:.2f}'
            )
        except Exception as e:
            self.get_logger().warn(f'Waiting for TF (map→base_footprint): {e}')

    # ──────────────────────────── return home ─────────────────────────────

    def _return_home(self):
        if self.home_pose is None:
            self.get_logger().error('Home pose is unknown – cannot navigate home.')
            return

        self._publish_status('returning_home')
        self.get_logger().info('Navigating back to home pose...')

        if not self._nav_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('Nav2 navigate_to_pose action server not available.')
            return

        goal = NavigateToPose.Goal()
        goal.pose = self.home_pose

        send_future = self._nav_client.send_goal_async(
            goal,
            feedback_callback=self._nav_feedback
        )
        send_future.add_done_callback(self._nav_goal_accepted)

    def _nav_feedback(self, feedback_msg):
        dist = feedback_msg.feedback.distance_remaining
        self.get_logger().info(
            f'Returning home – {dist:.2f} m remaining',
            throttle_duration_sec=3.0
        )

    def _nav_goal_accepted(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Return-home goal was rejected by Nav2.')
            return
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._nav_done)

    def _nav_done(self, future):
        self.get_logger().info('Arrived at home pose.  Map generation complete.')
        self._publish_status('done')
        # Publish home pose one more time so latecomers can read it
        if self.home_pose is not None:
            self._home_pub.publish(self.home_pose)

    # ──────────────────────────── helpers ─────────────────────────────────

    def _publish_status(self, status: str):
        msg = String()
        msg.data = status
        self._status_pub.publish(msg)
        self.get_logger().info(f'[status] → {status}')


# ──────────────────────────────── entry point ─────────────────────────────────

def main(args=None):
    rclpy.init(args=args)
    node = MapGenerationNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
