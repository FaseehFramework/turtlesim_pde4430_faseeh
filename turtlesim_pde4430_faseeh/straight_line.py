import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist  # Import the Twist message type

class MoveStraightNode(Node):
    def __init__(self):
        super().__init__('move_straight')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)


        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.get_logger().info('MoveStraight node started: Publishing straight line command.')

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 2.0  
        msg.angular.z = 0.0 
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    
    move_straight_node = MoveStraightNode()
    
    try:
        rclpy.spin(move_straight_node)
    except KeyboardInterrupt:
        pass  
    
    
    move_straight_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
