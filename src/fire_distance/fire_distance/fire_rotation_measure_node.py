import rclpy, time, math
from rclpy.node import Node
from std_msgs.msg import Float32, Bool
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu

class FireRotation(Node):
    def __init__(self):
        super().__init__('fire_rotation_measure_node')
        self.cx = None
        self.yaw0 = None
        self.create_subscription(Float32, '/fire_center_px', self.cx_cb, 10)
        self.create_subscription(Bool, '/fire/centered', self.centered_cb, 10)
        self.create_subscription(Imu, '/imu', self.imu_cb, 10)

        self.pub_cmd = self.create_publisher(Twist, '/cmd_vel', 10)
        self.pub_x0 = self.create_publisher(Float32, '/fire/x0_px', 10)
        self.pub_x1 = self.create_publisher(Float32, '/fire/x1_px', 10)
        self.pub_d = self.create_publisher(Float32, '/fire/actual_delta_deg', 10)

        self.state = 'IDLE'

    def cx_cb(self, msg):
        self.cx = msg.data

    def imu_cb(self, msg):
        q = msg.orientation
        self.yaw = math.degrees(math.atan2(2*(q.w*q.z), 1-2*q.z*q.z))

    def centered_cb(self, msg):
        if msg.data and self.state == 'IDLE':
            self.pub_x0.publish(Float32(data=self.cx))
            self.yaw0 = self.yaw
            self.state = 'ROT'
            self.start = time.time()

    def loop(self):
        if self.state == 'ROT':
            cmd = Twist()
            cmd.angular.z = 0.5
            self.pub_cmd.publish(cmd)
            if time.time() - self.start > 1.0:
                self.pub_cmd.publish(Twist())
                self.pub_x1.publish(Float32(data=self.cx))
                self.pub_d.publish(Float32(data=self.yaw - self.yaw0))
                self.state = 'IDLE'

def main():
    rclpy.init()
    node = FireRotation()
    node.create_timer(0.05, node.loop)
    rclpy.spin(node)
    rclpy.shutdown()
