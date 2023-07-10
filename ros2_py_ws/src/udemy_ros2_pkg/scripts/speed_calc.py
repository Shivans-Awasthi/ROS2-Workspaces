#!/usr/bin/env python3


import rclpy 
from rclpy.node import Node
from std_msgs.msg import Float32

WHEEL_RADIUS_DEFAULT=12.5 / 100

class SpeedCalculator(Node):
    def __init__(self):
        super().__init__("Speed_calc_node")
        self.declare_parameter("wheel_radius", WHEEL_RADIUS_DEFAULT)
        self.sub = self.create_subscription(Float32, "rpm", self.calculate_speed, 10)
        self.pub = self.create_publisher(Float32, "speed", 10)

  #      print(self.get_parameter("wheel_radius").get_parameter_value())

    def calculate_speed(self, rpm_msg):
        wheel_radius_param=self.get_parameter("wheel_radius").get_parameter_value().double_value
        speed = rpm_msg.data * wheel_radius_param * 2 * 3.14159 / 60 #speed in m/s
        speed_msg = Float32()
        speed_msg.data = float(speed)
        self.pub.publish(speed_msg) 
        


def main(args=None):
    rclpy.init()
    speed_calc=SpeedCalculator()
    print("Speed calculator Node Started..")

    try:
        rclpy.spin(speed_calc)
    except KeyboardInterrupt:
        print("Terminating Node..")
        speed_calc.destroy_node()


if __name__ == '__main__':
    main()