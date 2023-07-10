#!/usr/bin/env python3


import rclpy
from rclpy.node import Node

from udemy_ros2_pkg.srv import OddEvenCheck

class OddEvenCheckClient(Node):
    def __init__(self):
        super().__init__('Odd_Even_service_client_node')
        self.client=self.create_client(OddEvenCheck, 'odd_even_check')          #creating a client
        self.req=OddEvenCheck.Request()                                         #request service name


    def send_request(self,num):                                             #sending request
        self.req.number=int(num)
        self.client.wait_for_service()
        self.future=self.client.call_async(self.req)
        rclpy.spin_until_future_complete(self,self.future)

        self.result=self.future.result()
        return self.result                                              #geting result response
    


def main(args=None):
    rclpy.init()
    client_node=OddEvenCheckClient()					#function Calling
    print("OddEvenCheck service client Running..")

    try:
        user_input=input("Enter an integer: ")
        res=client_node.send_request(user_input)	
        print("Server returned: " + res.decision)			#keyboard interrupt for stopping Node 
    except KeyboardInterrupt:
        print("Terminating Node..")
        client_node.destroy_node()


if __name__ == '__main__':
    main()