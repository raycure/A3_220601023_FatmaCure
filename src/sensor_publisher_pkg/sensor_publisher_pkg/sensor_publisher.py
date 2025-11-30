#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random

class SensorPublisher(Node):
    def __init__(self):
        super().__init__('sensor_publisher')
        self.publisher_ = self.create_publisher(Float32, 'sensor_value', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.counter = 0
        self.get_logger().info('Sensor Publisher baslatildi')

    def timer_callback(self):
        msg = Float32()
        msg.data = random.uniform(0.0, 20.0)
        self.publisher_.publish(msg)
        self.get_logger().info(f'yayinlanan - "{msg.data:.2f}"')

def main(args=None):
    rclpy.init(args=args)
    node = SensorPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
