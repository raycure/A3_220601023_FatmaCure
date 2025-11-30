#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from command_server_pkg.srv import ComputeCommand

class CommandServer(Node):
    def __init__(self):
        super().__init__('command_server')
        self.srv = self.create_service(
            ComputeCommand,
            'compute_command',
            self.compute_callback)
        self.get_logger().info('Command Server baslatildi')

    def compute_callback(self, request, response):
        if request.input > 10.0:
            response.output = "HIGH"
        else:
            response.output = "LOW"
        self.get_logger().info(f'istek - "{request.input}" cavabi - "{response.output}"')
        return response

def main(args=None):
    rclpy.init(args=args)
    node = CommandServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
