import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class WebcamPublisher(Node):
    def __init__(self):
        super().__init__('webcam_publisher')
        self.publisher_ = self.create_publisher(Image, 'anafi/camera/image', 10)
        self.bridge = CvBridge()
        self.timer = self.create_timer(0.03, self.timer_callback)  # 10 Hz
        self.cap = cv2.VideoCapture(0)  # Abrir a webcam
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        if not self.cap.isOpened():
            self.get_logger().error('Unable to open webcam')
    
    def timer_callback(self):
        ret, frame = self.cap.read()

        if ret:
            # Converte a imagem de OpenCV para o formato ROS
            img_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            self.publisher_.publish(img_msg)
            self.get_logger().info('Publishing webcam image')
        else:
            self.get_logger().warn('No frame captured')

    def destroy(self):
        self.cap.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = WebcamPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
