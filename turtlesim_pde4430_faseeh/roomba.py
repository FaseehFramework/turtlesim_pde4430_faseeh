import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose  # 


STATE_FORWARD = 0
STATE_TURNING = 1


WALL_LIMIT_MIN = 0.5
WALL_LIMIT_MAX = 10.5


TURN_DURATION_S = 1.5 

class RoombaNode(Node):
    def __init__(self):
        super().__init__('roomba_cleaner')


        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        
        self.subscription_ = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,  
            10)

        
        timer_period = 0.1  # 10Hz
        self.timer = self.create_timer(timer_period, self.timer_callback)

        
        self.state = STATE_FORWARD
        self.turn_start_time = None

        self.get_logger().info('Roomba node started. Turtle will now bounce off walls.')

    def pose_callback(self, msg: Pose):
        

        
        if self.state == STATE_FORWARD:
            hit_wall = False
            if (msg.x < WALL_LIMIT_MIN or msg.x > WALL_LIMIT_MAX or
                msg.y < WALL_LIMIT_MIN or msg.y > WALL_LIMIT_MAX):
                hit_wall = True

            if hit_wall:
                
                self.state = STATE_TURNING
                
                self.turn_start_time = self.get_clock().now()
                self.get_logger().info('Hit a wall! Starting turn...')

    def timer_callback(self):
        
        cmd_msg = Twist()

        if self.state == STATE_FORWARD:
            
            cmd_msg.linear.x = 2.5
            cmd_msg.angular.z = 0.0

        elif self.state == STATE_TURNING:
            
            cmd_msg.linear.x = -0.5
            cmd_msg.angular.z = 1.8  # Turn at 1.8 rad/s

            
            now = self.get_clock().now()
            elapsed_time = (now - self.turn_start_time).nanoseconds / 1e9

            if elapsed_time > TURN_DURATION_S:
                
                self.state = STATE_FORWARD
                self.get_logger().info('Finished turn. Moving forward.')

        # Publish the command for the current state
        self.publisher_.publish(cmd_msg)


def main(args=None):
    rclpy.init(args=args)
    roomba_node = RoombaNode()
    try:
        rclpy.spin(roomba_node)
    except KeyboardInterrupt:
        pass

    roomba_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
