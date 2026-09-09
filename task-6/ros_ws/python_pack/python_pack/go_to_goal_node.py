import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

# TARGET_X = 10
# TARGET_Y = 10
# KP_LINEAR = 1.5
# KP_ANGULAR = 6

class GoToGoalNode(Node):
     def __init__(self):
        super().__init__("go_to_goal_node")
        # self.kp_linear = KP_LINEAR
        # self.kp_angular = KP_ANGULAR

        # self.target_x = TARGET_X
        # self.target_y = TARGET_Y

        # self.distance_tolerance = 0.1
        # self.angle_tolerance = 0.05

        self.declare_parameter('target_x', 10.0)
        self.declare_parameter('target_y', 10.0)
        self.declare_parameter('linear_gain', 1.5)
        self.declare_parameter('angular_gain', 6.0)
        self.declare_parameter('distance_tolerance', 0.1)
        self.declare_parameter('angle_tolerance', 0.05)
        self.declare_parameter('loop_rate_hz', 20.0)
 
        self.target_x = self.get_parameter('target_x').value
        self.target_y = self.get_parameter('target_y').value
        self.kp_linear = self.get_parameter('linear_gain').value
        self.kp_angular = self.get_parameter('angular_gain').value
        self.distance_tolerance = self.get_parameter('distance_tolerance').value
        self.angle_tolerance = self.get_parameter('angle_tolerance').value
        loop_rate_hz = self.get_parameter('loop_rate_hz').value

        self.current_pose = None
        self.goal_reached = False

        self.publisher = self.create_publisher(Twist,'/turtle1/cmd_vel',10)
        self.subscription = self.create_subscription( Pose, '/turtle1/pose', self.pose_callback, 10)
        self.create_timer(1.0 / loop_rate_hz, self.control_loop)

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


def main(args=None):
    rclpy.init(args=args)
    node = GoToGoalNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()