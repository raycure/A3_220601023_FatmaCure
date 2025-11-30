#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class DataProcessor(Node):
    def __init__(self):
        super().__init__('data_processor')
        self.subscription = self.create_subscription(
            Float32,
            'sensor_value',
            self.listener_callback,
            10)
        self.publisher_ = self.create_publisher(Float32, 'processed_value', 10)
        self.get_logger().info('Data Processor baslatildi')

    def listener_callback(self, msg):
        processed_msg = Float32()
        processed_msg.data = msg.data * 2.0
        self.publisher_.publish(processed_msg)
        self.get_logger().info(f'alinan - "{msg.data:.2f}" islenen - "{processed_msg.data:.2f}"')

def main(args=None):
    rclpy.init(args=args)
    node = DataProcessor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
