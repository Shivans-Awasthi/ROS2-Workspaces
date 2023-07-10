#!/usr/bin/env python3


import rclpy 
from rclpy.node import Node
from std_msgs.msg import String

class HelloWorldSubscriber(Node):			
    def __init__(self):
        super().__init__("Hello_world_sub_node")
        self.sub = self.create_subscription(String, "hello_world", self.subscriber_callback, 10)	#subscriber Node to the topic hello_world

    def subscriber_callback(self, msg):			#after recieving action
        print("Recieved: " + msg.data)



def main(args=None):
    rclpy.init()
    my_sub=HelloWorldSubscriber()			#function calling
    print("Waiting for data to be published..")

    try:
        rclpy.spin(my_sub)
    except KeyboardInterrupt:				#keyboard interrupt for stopping the node
        print("Terminating Node..")
        my_sub.destroy_node()


if __name__ == '__main__':
    main()
