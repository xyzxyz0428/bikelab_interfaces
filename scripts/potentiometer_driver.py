#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from bikelab_interfaces.msg import AdcData
import smbus
from std_msgs.msg import Header
import time

class PotentiometerDriver(Node):
    def __init__(self):
        super().__init__('potentiometer_driver')
        self.publisher_ = self.create_publisher(AdcData, 'adc_data', 10)
        self.ADC = smbus.SMBus(1)  # Setup I2C communication on bus 1
        self.timer = self.create_timer(1.0, self.timer_callback)  # Create a timer to call the callback every 1 second

    def timer_callback(self):
        try:
            self.ADC.write_byte(0x24, 0x10)  # Write a byte to the slave
            data_value = self.ADC.read_word_data(0x24, 0x10)  # Read data from the ADC
            self.get_logger().info("Data read from ADC: {}".format(data_value))

            # Create a message and assign the data and timestamp
            msg = AdcData()
            msg.header = Header()
            msg.header.stamp = self.get_clock().now().to_msg()  # Set the timestamp
            msg.data = float(-90+180/657*data_value)
            self.get_logger().info("Data published: {}".format(msg.data))


            self.publisher_.publish(msg)  # Publish the message
        except Exception as e:
            self.get_logger().error("Error reading ADC data: {}".format(e))

def main(args=None):
    rclpy.init(args=args)  # Initialize the ROS communication
    potentiometer_driver = PotentiometerDriver()  # Create the ROS node
    rclpy.spin(potentiometer_driver)  # Keep the node alive to listen to callbacks
    potentiometer_driver.destroy_node()  # Cleanup the node
    rclpy.shutdown()  # Shutdown ROS communication

if __name__ == '__main__':
    main()
