import rclpy, json
from rclpy.node import Node
from std_msgs.msg import Float32, String

class FireDistanceController(Node):
    def __init__(self):
        super().__init__('fire_distance_controller_node')
        self.x0 = self.x1 = self.d = None
        self.create_subscription(Float32, '/fire/x0_px', self.x0_cb, 10)
        self.create_subscription(Float32, '/fire/x1_px', self.x1_cb, 10)
        self.create_subscription(Float32, '/fire/actual_delta_deg', self.d_cb, 10)
        self.pub = self.create_publisher(String, '/fire/distance_batch', 10)

    def x0_cb(self, m): self.x0 = m.data
    def x1_cb(self, m): self.x1 = m.data
    def d_cb(self, m):
        self.d = m.data
        if self.x0 and self.x1:
            dist = abs(self.x1 - self.x0)
            self.pub.publish(String(data=json.dumps({"pixel_delta": dist})))

def main():
    rclpy.init()
    rclpy.spin(FireDistanceController())
    rclpy.shutdown()
