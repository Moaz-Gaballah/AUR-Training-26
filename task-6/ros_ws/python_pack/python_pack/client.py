import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class client(Node):

    def __init__(self):
        super().__init__('client')

        self.declare_parameter('delay_seconds', 3.0)
        self.delay_seconds = self.get_parameter('delay_seconds').value

        self.client = self.create_client(SetBool, 'toggle_movement')

        self.delay_timer = self.create_timer(self.delay_seconds, self.on_delay_elapsed)

        self.get_logger().info(f'Will call toggle_movement in {self.delay_seconds:.1f} seconds...')

    def on_delay_elapsed(self):
        self.delay_timer.cancel()  

        if not self.client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error('service not available.')
            return

        request = SetBool.Request()
        request.data = True

        future = self.client.call_async(request)
        future.add_done_callback(self.on_response)

    def on_response(self, future):
        
          response = future.result()
          self.get_logger().info(
               f'Service call result: success={response.success}, message="{response.message}"'
          )



def main(args=None):
    rclpy.init(args=args)
    node = client()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

