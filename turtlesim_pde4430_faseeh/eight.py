import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class MoveFigureEightNode(Node):
    def __init__(self):
        super().__init__('move_figure_eight')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # --- Parameters ---
        self.LINEAR_VEL = 2.0  
        self.ANGULAR_VEL = 1.0 



        self.switch_duration = 2 * math.pi / self.ANGULAR_VEL 


        self.start_time = self.get_clock().now()


        timer_period = 0.1  
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.get_logger().info(f'Eight node started. Switching turn every {self.switch_duration:.2f} seconds.')
        self.current_angular_vel = self.ANGULAR_VEL

    def timer_callback(self):
        msg = Twist()

        elapsed_seconds = (self.get_clock().now() - self.start_time).nanoseconds / 1e9

        if int(elapsed_seconds // self.switch_duration) % 2 == 0:
            self.current_angular_vel = self.ANGULAR_VEL
        else:
            self.current_angular_vel = -self.ANGULAR_VEL

        msg.linear.x = self.LINEAR_VEL
        msg.angular.z = self.current_angular_vel

        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    move_figure_eight_node = MoveFigureEightNode()
    try:
        rclpy.spin(move_figure_eight_node)
    except KeyboardInterrupt:
        pass

    move_figure_eight_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
