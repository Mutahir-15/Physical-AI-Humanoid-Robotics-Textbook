import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import StaticTransformBroadcaster
import tf_transformations

class StaticFramePublisher(Node):
    def __init__(self):
        super().__init__('static_broadcaster')

        self.tf_static_broadcaster = StaticTransformBroadcaster(self)

        # Create a static transform from 'base_link' to 'camera_link'
        static_transform_stamped = TransformStamped()
        static_transform_stamped.header.stamp = self.get_clock().now().to_msg()
        static_transform_stamped.header.frame_id = 'base_link'
        static_transform_stamped.child_frame_id = 'camera_link'
        static_transform_stamped.transform.translation.x = 0.1
        static_transform_stamped.transform.translation.y = 0.0
        static_transform_stamped.transform.translation.z = 0.2

        quat = tf_transformations.quaternion_from_euler(0.0, 0.0, 0.0)
        static_transform_stamped.transform.rotation.x = quat[0]
        static_transform_stamped.transform.rotation.y = quat[1]
        static_transform_stamped.transform.rotation.z = quat[2]
        static_transform_stamped.transform.rotation.w = quat[3]

        self.tf_static_broadcaster.sendTransform(static_transform_stamped)
        self.get_logger().info('Published static transform from base_link to camera_link')

def main():
    rclpy.init()
    node = StaticFramePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
