import rclpy
from rclpy.node import Node
from std_msgs.msg import String # Example message type

class SimpleSubscriber(Node):
    def __init__(self):
        super().__init__('simple_subscriber_node')
        self.subscription = self.create_subscription(
            String,
            'my_topic', # Must match the publisher's topic name
            self.listener_callback,
            10) # Queue size
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = SimpleSubscriber()
    rclpy.spin(minimal_subscriber) # Keep node alive until Ctrl+C
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
