import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

TARGET_X = 10
TARGET_Y = 10
KP_LINEAR = 1.5
KP_ANGULAR = 6

class GoToGoalNode(Node):
     def __init__(self):
        super().__init__("go_to_goal_node")
        self.kp_linear = KP_LINEAR
        self.kp_angular = KP_ANGULAR

        self.target_x = TARGET_X
        self.target_y = TARGET_Y

        self.distance_tolerance = 0.1
        self.angle_tolerance = 0.05

        self.current_pose = None
        self.goal_reached = False

        self.publisher = self.create_publisher(Twist,'/turtle1/cmd_vel',10)
        self.subscription = self.create_subscription( Pose, '/turtle1/pose', self.pose_callback, 10)
        self.timer = self.create_timer(0.05, self.control_loop)

     def pose_callback(self, msg):
          self.current_pose = msg

     def normalize_angle(self, angle):
        while angle > math.pi:
          angle -= 2 * math.pi
        while angle < -math.pi:
          angle += 2 * math.pi
        return angle

     
 
     def control_loop(self):
        if self.current_pose is None or self.goal_reached:
          return

        dx = self.target_x - self.current_pose.x
        dy = self.target_y - self.current_pose.y
        distance_error = math.sqrt(dx ** 2 + dy ** 2)

        target_angle = math.atan2(dy, dx)
        heading_error = self.normalize_angle(target_angle - self.current_pose.theta)

        if distance_error < self.distance_tolerance:
          self.publisher.publish(Twist())  
          self.goal_reached = True
          self.get_logger().info('Goal reached')
          return

        twist = Twist()
        if abs(heading_error) > self.angle_tolerance:
          twist.linear.x = 0.0
          twist.angular.z = self.kp_angular * heading_error
        else:
          twist.linear.x = min(self.kp_linear * distance_error, 2.0)
          twist.angular.z = self.kp_angular * heading_error

        self.publisher.publish(twist)


def main():
    rclpy.init()
    node = GoToGoalNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()