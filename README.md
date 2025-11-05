# pde4430_turtlesim_formativeExercise
turtlesim simulation formative exercise practice

## TASK1 : DISCOVERIES
1. What is the name of the publisher node?
   teleop_turtle
2. What is the message type of /cmd_vel?
   geometry_msgs/msg/Twist
3. WHat is the frequency of publication of the node publishing on /cmd_vel?
   ros2 topic hz /turtle1/cmd_vel
average rate: 23.029
	min: 0.029s max: 0.501s std dev: 0.07840s window: 35
4. What is the message type of /turtle1/pose ?
   Type: turtlesim/msg/Pose
5. Give an example of a message that is being published on /turtlel/color_sensor. Display the contents of the topic in a terminal window and copy-paste.
   r: 179
  g: 184
  b: 255
   
  r: 179
  g: 184
  b: 255
  
  r: 179
  g: 184
  b: 255
  ---
**setup**
1. ensure this package (turtlesim_pde4430_faseeh) is located in your src in your ROS 2 workspace
2. Navigate to the root of your workspace and build the package
 `colcon build --packages-select turtlesim_pde4430_faseeh`
3. dont forget to source your workspace's setup file
   `source install/setup.bash `
   ---
### For all exercises, you must have the TurtleSim simulator running in its own terminal. `ros2 run turtlesim turtlesim_node`
---
## TASK 2
1. What it does: Moves the turtle forward in a straight line indefinitely.
How to Run: `ros2 run turtlesim_pde4430_fas gostr`
2. What it does: Moves the turtle in a continuous circle at a fixed radius.
How to Run: `ros2 run turtlesim_pde4430_fas gocircle`
3. What it does: Moves the turtle in a continuous figure-eight pattern by reversing its angular velocity after a set time.
How to Run: `ros2 run turtlesim_pde4430_fas go8`
4. What it does: A roomba. The turtle moves straight until it detects a wall, then reverses and turns to a new direction.
How to Run: `ros2 run turtlesim_pde4430_fas goroomba`
5. What it does: A lawn mower. The turtle spawns at 4 corners and cleans the entire area in an S pattern.
How to Run: `ros2 run turtlesim_pde4430_fas roomba4x`
---
## TASK 3
1. What it does: Prompts the user in the terminal at startup to enter a desired linear and angular speed. It then drives the turtle at those speeds.
How to Run: `ros2 run turtlesim_pde4430_fas user_go`
2. What it does: Prompts the user in the terminal at startup for a target (X, Y) coordinate. It uses a Proportional controller to autonomously navigate the turtle to that goal and then stops.
How to Run: `ros2 run turtlesim_pde4430_fas go_goal`
