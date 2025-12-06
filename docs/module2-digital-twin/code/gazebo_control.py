import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist

class GazeboControlNode(Node):
    def __init__(self):
        super().__init__('gazebo_control_node')

        # Publisher for joint control (conceptual, actual topic depends on ros2_control setup)
        self.joint_publisher = self.create_publisher(Float64, '/my_robot_joint_controller/commands', 10)
        self.joint_position = 0.0
        self.joint_timer = self.create_timer(1.0, self.publish_joint_command)

        # Subscriber for joint states
        self.joint_state_subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        # Publisher for base velocity control
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.cmd_vel_timer = self.create_timer(2.0, self.publish_cmd_vel)

        self.get_logger().info('Gazebo Control Node started.')

    def publish_joint_command(self):
        msg = Float64()
        self.joint_position = 0.5 if self.joint_position == 0.0 else 0.0 # Example: toggle position
        msg.data = self.joint_position
        self.joint_publisher.publish(msg)
        self.get_logger().info(f'Publishing joint command: {msg.data}')

    def joint_state_callback(self, msg):
        # Example: print received joint states
        if msg.name:
            for i, name in enumerate(msg.name):
                self.get_logger().info(f'Joint: {name}, Position: {msg.position[i]:.2f}')

    def publish_cmd_vel(self):
        msg = Twist()
        msg.linear.x = 0.1 # Move forward
        msg.angular.z = 0.0 # No rotation
        self.cmd_vel_publisher.publish(msg)
        self.get_logger().info(f'Publishing /cmd_vel: Linear.x={msg.linear.x}')


def main(args=None):
    rclpy.init(args=args)
    node = GazeboControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
