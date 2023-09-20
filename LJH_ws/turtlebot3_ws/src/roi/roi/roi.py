import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class Roi(Node):

    def __init__(self):
        super().__init__('roi')
        self.scan_ranges = []
        self.init_scan_state = False

        self.scan_sub = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,5)

    def scan_callback(self, msg):
        self.scan_ranges = msg.ranges
        self.init_scan_state = True
        print(msg.angle_min)


def main(args=None):
    rclpy.init(args=args)
    node = Roi()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    
    main()
