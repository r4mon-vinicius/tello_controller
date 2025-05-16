from tello_controller.tello_zune import TelloZune
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

tello = TelloZune()
tello.start_tello()

class TelloCam(Node):
    def __init__(self):
        super().__init__('tello_cam')
        self.publisher = self.create_publisher(Image, 'tello_image', 10)
        self.bridge = CvBridge()
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        try:
            frame = tello.get_frame()
            if frame is not None:
                img_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
                self.publisher.publish(img_msg)
                self.get_logger().info('Publishing Tello image')
            else:
                self.get_logger().warn('No frame captured')
        except Exception as e:
            self.get_logger().error(f"Failed to get frame: {e}")

    def destroy(self):
        super().destroy_node()
        tello.end_tello()

def main(args=None):
    rclpy.init(args=args)
    node = TelloCam()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
