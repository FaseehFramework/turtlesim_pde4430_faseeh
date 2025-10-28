import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import TeleportAbsolute
import math

# State constants
STATE_MOVING_ACROSS = 0
STATE_TURNING_1 = 1
STATE_MOVING_DOWN = 2
STATE_TURNING_2 = 3

# Direction constants
DIR_RIGHT = 1
DIR_LEFT = -1

# Parameters
TURN_ANGULAR_VEL = 1.57  # 90 deg/s
TURN_DURATION_90_DEG = 1.0
LANE_WIDTH = 0.5
FORWARD_VEL_DOWN = 0.5
MOVE_DOWN_DURATION = LANE_WIDTH / FORWARD_VEL_DOWN
FORWARD_VEL_ACROSS = 3.0

class LawnmowerNode(Node):
    def __init__(self):
        # Give the node a unique name (it will be overridden by __node:=... on launch)
        super().__init__('lawnmower_cleaner_node')

        # --- NEW: Declare parameters ---
        self.declare_parameter('turtle_name', 'turtle1')
        self.declare_parameter('start_x', 1.0)
        self.declare_parameter('start_y', 10.0)
        self.declare_parameter('start_theta', 0.0)
        self.declare_parameter('vertical_direction', 'down') # 'up' or 'down'

        # --- NEW: Get parameters ---
        self.turtle_name = self.get_parameter('turtle_name').get_parameter_value().string_value
        self.start_x = self.get_parameter('start_x').get_parameter_value().double_value
        self.start_y = self.get_parameter('start_y').get_parameter_value().double_value
        self.start_theta = self.get_parameter('start_theta').get_parameter_value().double_value
        self.vertical_direction = self.get_parameter('vertical_direction').get_parameter_value().string_value

        # Set multipliers based on parameters
        self.direction = DIR_RIGHT if self.start_theta == 0.0 else DIR_LEFT
        self.vert_turn_multiplier = -1.0 if self.vertical_direction == 'down' else 1.0

        self.get_logger().info(f'Starting cleaner for {self.turtle_name} at ({self.start_x}, {self.start_y})')

        # --- NEW: Dynamic topic and service names ---
        cmd_vel_topic = f'/{self.turtle_name}/cmd_vel'
        pose_topic = f'/{self.turtle_name}/pose'
        teleport_service = f'/{self.turtle_name}/teleport_absolute'

        self.publisher_ = self.create_publisher(Twist, cmd_vel_topic, 10)
        self.subscription_ = self.create_subscription(
            Pose, pose_topic, self.pose_callback, 10)

        self.teleport_client = self.create_client(TeleportAbsolute, teleport_service)
        while not self.teleport_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(f'Teleport service for {self.turtle_name} not available, waiting...')

        # --- State and logic variables ---
        self.state = STATE_MOVING_ACROSS
        self.state_start_time = self.get_clock().now()

        self.go_to_start_pos()
        self.timer = self.create_timer(0.05, self.timer_callback)

    def go_to_start_pos(self):
        # Use parameters to teleport
        req = TeleportAbsolute.Request()
        req.x = self.start_x
        req.y = self.start_y
        req.theta = self.start_theta
        self.teleport_client.call_async(req)

    def pose_callback(self, msg: Pose):
        if self.state != STATE_MOVING_ACROSS:
            return

        hit_wall = False
        if self.direction == DIR_RIGHT and msg.x > 10.5:
            hit_wall = True
        elif self.direction == DIR_LEFT and msg.x < 0.5:
            hit_wall = True

        if hit_wall:
            self.get_logger().info(f'[{self.turtle_name}] Hit wall, starting S-turn.')
            self.state = STATE_TURNING_1
            self.state_start_time = self.get_clock().now()

    def timer_callback(self):
        cmd_msg = Twist()
        now = self.get_clock().now()
        elapsed_state_time = (now - self.state_start_time).nanoseconds / 1e9

        # --- NEW: Modified turn logic ---
        # This logic makes the turtle turn "down" or "up" based on the multiplier
        turn_angular_z = self.vert_turn_multiplier * TURN_ANGULAR_VEL * self.direction

        if self.state == STATE_MOVING_ACROSS:
            cmd_msg.linear.x = FORWARD_VEL_ACROSS
            cmd_msg.angular.z = 0.0

        elif self.state == STATE_TURNING_1:
            cmd_msg.linear.x = 0.0
            cmd_msg.angular.z = turn_angular_z

            if elapsed_state_time > TURN_DURATION_90_DEG:
                self.state = STATE_MOVING_DOWN
                self.state_start_time = now

        elif self.state == STATE_MOVING_DOWN:
            cmd_msg.linear.x = FORWARD_VEL_DOWN
            cmd_msg.angular.z = 0.0

            if elapsed_state_time > MOVE_DOWN_DURATION:
                self.state = STATE_TURNING_2
                self.state_start_time = now

        elif self.state == STATE_TURNING_2:
            cmd_msg.linear.x = 0.0
            cmd_msg.angular.z = turn_angular_z

            if elapsed_state_time > TURN_DURATION_90_DEG:
                self.state = STATE_MOVING_ACROSS
                self.direction = self.direction * -1 # Flip direction
                self.state_start_time = now
                dir_str = "LEFT" if self.direction == -1 else "RIGHT"
                self.get_logger().info(f'[{self.turtle_name}] Turn complete. Moving {dir_str}.')

        self.publisher_.publish(cmd_msg)

def main(args=None):
    rclpy.init(args=args)
    lawnmower_node = LawnmowerNode()
    try:
        rclpy.spin(lawnmower_node)
    except KeyboardInterrupt:
        pass

    lawnmower_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
