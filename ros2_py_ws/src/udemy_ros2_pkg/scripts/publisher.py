#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class HelloWorldPublisher(Node):
    def __init__(self):
        super().__init__("Hello_world_pub_node")
        self.pub = self.create_publisher(String, "hello_world", 10)      #Publisher created with topic name hello_world
        self.timer = self.create_timer(0.5, self.publish_hello_world)	 #Timer for publishing
        self.counter = 0						

    def publish_hello_world(self):
        msg = String()							#msg datatype string
        msg.data = "Hello World " + str(self.counter)			#data
        self.pub.publish(msg) 						#counter incremented
        self.counter += 1

def main(args=None):
    rclpy.init()
    my_pub=HelloWorldPublisher()					#function Calling
    print("Publisher Node Running")

    try:
        rclpy.spin(my_pub)						#keyboard interrupt for stopping Node 
    except KeyboardInterrupt:
        print("Terminating Node..")
        my_pub.destroy_node()


if __name__ == '__main__':
    main()
