import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from tf2_msgs.msg import TFMessage
import tf2_ros

class ImuSubscriber(Node):
    def __init__(self):
        super().__init__('imu_subscriber')
        self.subscription = self.create_subscription(Imu, 'imu_data', self.imu_callback, 10)
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)

    def imu_callback(self, msg):
        # Create a transform message with the IMU orientation
        transform_stamped = tf2_ros.TransformStamped()
        transform_stamped.header.stamp = msg.header.stamp
        transform_stamped.header.frame_id = 'world'
        transform_stamped.child_frame_id = 'imu_link'
        transform_stamped.transform.translation.x = 0.0
        transform_stamped.transform.translation.y = 0.0
        transform_stamped.transform.translation.z = 0.0
        transform_stamped.transform.rotation = msg.orientation
        tf_msg = TFMessage()
        tf_msg.transforms.append(transform_stamped)
        self.tf_broadcaster.sendTransform(tf_msg.transforms)

def main(args=None):
    rclpy.init(args=args)
    imu_subscriber = ImuSubscriber()
    rclpy.spin(imu_subscriber)
    imu_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()