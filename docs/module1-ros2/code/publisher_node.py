import rclpy
from rclpy.node import Node
from std_msgs.msg import String # Example message type

class SimplePublisher(Node):
    def __init__(self):
        super().__init__('simple_publisher_node')
        self.publisher_ = self.create_publisher(String, 'my_topic', 10) # Topic name, message type, queue size
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello ROS 2 World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = SimplePublisher()
    rclpy.spin(minimal_publisher) # Keep node alive until Ctrl+C
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
