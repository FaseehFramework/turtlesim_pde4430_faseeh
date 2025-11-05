import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math 
K_LINEAR = 1.5  
K_ANGULAR = 6.0 
GOAL_TOLERANCE = 0.1 
class MoveToGoalNode(Node):
    def __init__(self):
        super().__init__('move_to_goal')
        
        self.get_logger().info('Node started. Please provide a goal coordinate.')
        try:
            self.goal_x = float(input("Enter goal X coordinate (e.g., 8.0): "))
            self.goal_y = float(input("Enter goal Y coordinate (e.g., 2.5): "))
        except ValueError:
            self.get_logger().error('Invalid input. Shutting down.')
            rclpy.try_shutdown()
            return
        
        self.get_logger().info(f'Goal set to: X={self.goal_x}, Y={self.goal_y}')

        self.current_pose = None
        self.goal_reached = False
        
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        self.subscription_ = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10)
        
        self.timer = self.create_timer(0.1, self.control_loop_callback) 

    def pose_callback(self, msg: Pose):
        self.current_pose = msg

    def control_loop_callback(self):
        
        if self.current_pose is None or self.goal_reached:
            return
            
        
        dx = self.goal_x - self.current_pose.x
        dy = self.goal_y - self.current_pose.y
        distance = math.sqrt(dx**2 + dy**2)
        
        angle_to_goal = math.atan2(dy, dx)
        
        angle_error = angle_to_goal - self.current_pose.theta
        angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))
        
        cmd_msg = Twist()
        
        if distance < GOAL_TOLERANCE:
            self.goal_reached = True
            cmd_msg.linear.x = 0.0
            cmd_msg.angular.z = 0.0

            self.publisher_.publish(cmd_msg)
            
            self.get_logger().info('Goal reached')
            
            self.timer.cancel()
            
            rclpy.try_shutdown()
            
            return 
        
        elif abs(angle_error) > GOAL_TOLERANCE:
            cmd_msg.linear.x = 0.0
            cmd_msg.angular.z = K_ANGULAR * angle_error
        else:
            cmd_msg.linear.x = K_LINEAR * distance
            cmd_msg.angular.z = 0.0
        
        self.publisher_.publish(cmd_msg)

def main(args=None):
    rclpy.init(args=args)
    move_to_goal_node = MoveToGoalNode()
    
    try:
        rclpy.spin(move_to_goal_node)
    except KeyboardInterrupt:
        pass
    except rclpy.executors.ExternalShutdownException:
        pass
    
    move_to_goal_node.destroy_node()

if __name__ == '__main__':
    main()