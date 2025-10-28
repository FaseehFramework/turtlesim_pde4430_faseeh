import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MoveInCircleNode(Node):
    def __init__(self):
        super().__init__('move_in_circle')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        timer_period = 0.1  
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.get_logger().info('Publishing circle command')

    def timer_callback(self):
        msg = Twist()

        msg.linear.x = 2.0


        msg.angular.z = 1.0

        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    move_in_circle_node = MoveInCircleNode()

    try:
        rclpy.spin(move_in_circle_node)
    except KeyboardInterrupt:
        pass

    move_in_circle_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
