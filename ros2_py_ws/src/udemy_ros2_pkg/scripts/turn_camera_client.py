#!/usr/bin/env python3


from numpy import float32
import rclpy
from rclpy.node import Node

import cv2
from cv_bridge import CvBridge
 

from udemy_ros2_pkg.srv import TurnCamera

class TurnCameraClient(Node):
    def __init__(self):
        super().__init__('Turn_camera_service_client_node')
        self.client=self.create_client(TurnCamera, 'turn_camera')
        self.req=TurnCamera.Request()


    def send_request(self,imageangle):
        self.req.angle=float(imageangle)
        self.client.wait_for_service()
        self.future=self.client.call_async(self.req)
        rclpy.spin_until_future_complete(self,self.future)

        self.result=self.future.result()

        return self.result.image
     

    def display_image(self, image_msg):
        image=CvBridge().imgmsg_to_cv2(image_msg)
        cv2.imshow("The response Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()		
    


def main(args=None):
    rclpy.init()
    client_node=TurnCameraClient()					#function Calling
    print("TurnCamera service client Running..")

    try:
        user_input=input("Enter an angle(0,15,30): ")
        res=client_node.send_request(user_input)
        client_node.display_image(res)	
        
      #keyboard interrupt for stopping Node 
    except KeyboardInterrupt:
        print("Terminating Node..")
        client_node.destroy_node()


if __name__ == '__main__':
    main()