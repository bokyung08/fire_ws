import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
import cv2
import onnxruntime as ort
import numpy as np

class FireDetectorONNX(Node):
    def __init__(self):
        super().__init__('fire_detector_onnx')
        self.pub = self.create_publisher(Bool, '/fire_detected', 10)

        self.cap = cv2.VideoCapture(0)
        self.session = ort.InferenceSession(
            '/home/ubuntu/best.onnx',
            providers=['CPUExecutionProvider']
        )

        self.timer = self.create_timer(0.1, self.run)

    def run(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        img = cv2.resize(frame, (320, 320))
        img = img.transpose(2, 0, 1) / 255.0
        img = np.expand_dims(img, axis=0).astype(np.float32)

        outputs = self.session.run(None, {'images': img})
        fire_detected = len(outputs[0]) > 0

        self.pub.publish(Bool(data=fire_detected))

def main():
    rclpy.init()
    rclpy.spin(FireDetectorONNX())
    rclpy.shutdown()
