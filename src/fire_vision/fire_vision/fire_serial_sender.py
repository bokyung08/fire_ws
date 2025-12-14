import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
import serial

class FireSerialSender(Node):
    def __init__(self):
        super().__init__('fire_serial_sender')
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        self.create_subscription(Bool, '/fire_detected', self.callback, 10)

    def callback(self, msg):
        if msg.data:
            self.ser.write(b'1')
            self.get_logger().info('Fire detected -> Serial sent')

def main():
    rclpy.init()
    rclpy.spin(FireSerialSender())
    rclpy.shutdown()
