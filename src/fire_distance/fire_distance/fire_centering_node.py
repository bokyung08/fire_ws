import rclpy, time
from rclpy.node import Node
from std_msgs.msg import Float32, Bool
from geometry_msgs.msg import Twist

WIDTH_PX = 640
KP = 3.0
DEADBAND = 0.06

class FireCentering(Node):
    def __init__(self):
        super().__init__('fire_centering_node')
        self.cx = None
        self.pub_cmd = self.create_publisher(Twist, '/cmd_vel', 10)
        self.pub_centered = self.create_publisher(Bool, '/fire/centered', 10)
        self.create_subscription(Float32, '/fire_center_px', self.cb, 10)
        self.timer = self.create_timer(0.05, self.loop)

    def cb(self, msg):
        self.cx = msg.data

    def loop(self):
        if self.cx is None:
            return
        err = (self.cx - WIDTH_PX/2) / WIDTH_PX
        cmd = Twist()
        if abs(err) < DEADBAND:
            self.pub_centered.publish(Bool(data=True))
        else:
            cmd.angular.z = max(min(KP * err, 1.0), -1.0)
        self.pub_cmd.publish(cmd)

def main():
    rclpy.init()
    rclpy.spin(FireCentering())
    rclpy.shutdown()

