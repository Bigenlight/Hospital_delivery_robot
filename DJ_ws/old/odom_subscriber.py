import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from tf2_msgs.msg import TFMessage
import tf2_ros

class OdomSubscriber(Node):
    def __init__(self):
        super().__init__('odom_subscriber')
        self.subscription = self.create_subscription(Odometry, 'odom_data', self.odom_callback, 10)
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)

    def odom_callback(self, msg):
        # Create a transform message with the Odometry pose
        transform_stamped = tf2_ros.TransformStamped()
        transform_stamped.header.stamp = msg.header.stamp
        transform_stamped.header.frame_id = 'world'
        transform_stamped.child_frame_id = 'odom_link'
        transform_stamped.transform.translation.x = msg.pose.pose.position.x
        transform_stamped.transform.translation.y = msg.pose.pose.position.y
        transform_stamped.transform.translation.z = 0.0
        transform_stamped.transform.rotation = msg.pose.pose.orientation
        tf_msg = TFMessage()
        tf_msg.transforms.append(transform_stamped)
        self.tf_broadcaster.sendTransform(tf_msg.transforms)

def main(args=None):
    rclpy.init(args=args)
    odom_subscriber = OdomSubscriber()
    rclpy.spin(odom_subscriber)
    odom_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()