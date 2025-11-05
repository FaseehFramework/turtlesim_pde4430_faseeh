import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MoveWithInputNode(Node):
    def __init__(self):
        super().__init__('move_with_input')

        self.get_logger().info('provide speed values.')

        try:
            linear_vel = float(input("linear speed (e.g., 2.0): "))
        except ValueError:
            self.get_logger().warn('Invalid input. Defaulting linear speed to 1.0')
            linear_vel = 1.0

        try:
            angular_vel = float(input("Enter angular speed (e.g., 1.5): "))
        except ValueError:
            self.get_logger().warn('Invalid input. Defaulting angular speed to 0.0')
            angular_vel = 0.0

        self.get_logger().info(f'Speeds set Linear: {linear_vel}, Angular: {angular_vel}')

        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.twist_msg_ = Twist()
        self.twist_msg_.linear.x = linear_vel
        self.twist_msg_.angular.z = angular_vel

        timer_period = 0.1  
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        self.publisher_.publish(self.twist_msg_)

def main(args=None):
    rclpy.init(args=args)
    move_with_input_node = MoveWithInputNode()

    try:
        rclpy.spin(move_with_input_node)
    except KeyboardInterrupt:
        pass

    move_with_input_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
