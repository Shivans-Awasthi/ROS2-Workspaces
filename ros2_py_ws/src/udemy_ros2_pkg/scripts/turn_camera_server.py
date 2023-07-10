#!/usr/bin/env python3


import os
import rclpy
from rclpy.node import Node
import cv2
from cv_bridge import CvBridge

from udemy_ros2_pkg.srv import TurnCamera

class TurnCameraServer(Node):
    def __init__(self):
        super().__init__('Turn_camera_service_server_node')
        self.available_angles = [-30, -15, 0, 15, 30]
        self.srv=self.create_service(TurnCamera, 'turn_camera',self.return_image)


    def return_image(self,request,response):
        image=self.get_image(request.angle)
        image_msg=CvBridge().cv2_to_imgmsg(image)

        response.image=image_msg
        return response

    
    def get_image(self,angle):
        closest_angle=min(self.available_angles,key=lambda x:abs(x-angle))
        print(closest_angle)
        return self.read_in_image_by_filename(str(closest_angle) + ".png")


    def read_in_image_by_filename(self, file_name):
        dir_name=os.path.dirname(__file__)
        install_dir_index=dir_name.index("install/")
        file_location=dir_name[0:install_dir_index] + "src/udemy_ros2_pkg/Images/" + file_name

       
        image=cv2.imread(file_location)
        return image
       

def main(args=None):
    rclpy.init()
    server_node=TurnCameraServer()					#function Calling
    print("Turn_camera service server Running..")

    try:
        rclpy.spin(server_node)						#keyboard interrupt for stopping Node 
    except KeyboardInterrupt:
        print("Terminating Node..")
        server_node.destroy_node()


if __name__ == '__main__':
    main()