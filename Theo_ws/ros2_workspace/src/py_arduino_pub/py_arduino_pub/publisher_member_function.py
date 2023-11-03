import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'detected_object', 10)
        timer_period = 0.0005  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.order = "rest "
        
        #
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = self.order
        self.publisher_.publish(msg)
        self.get_logger().info('Sending order to Python: "%s"' % msg.data)
        
        #
        # self.i += 1
        # if(self.i % 5000 < 1000): self.order = "push "
        # elif(self.i % 5000 > 2000 and self.i % 5000 < 3000): self.order = "pull "
        # else : self.order = "rest "
        
        self.i += 1
        if(self.i % 6000 > 1000 and self.i % 6000 < 2000): self.order = "lo "
        elif(self.i % 6000 > 4000 and self.i % 6000 < 5000): self.order = "un "  
        elif(self.i % 3000 < 100): self.order = "push "
        #elif(self.i % 5000 > 2000 and self.i % 5000 < 3000): self.order = "pull "
        else : self.order = "rest "
        


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
