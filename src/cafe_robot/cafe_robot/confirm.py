import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool


class Confirm(Node):

    def __init__(self):

        super().__init__("confirm")

        self.kitchen_confirmed = False
        self.table_confirmed = False

        self.create_subscription(
            Bool,
            "/confirm",
            self.confirm_callback,
            10
        )

    def confirm_callback(self, msg):

        self.kitchen_confirmed = msg.data
        self.table_confirmed = msg.data