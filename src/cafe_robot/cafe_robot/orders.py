import rclpy

from rclpy.node import Node

from std_msgs.msg import String


class Orders(Node):

    def __init__(self):

        super().__init__("orders")

        self.create_subscription(
            String,
            "/order",
            self.order_callback,
            10
        )

    def order_callback(self, msg):

        self.get_logger().info(
            f"New order : {msg.data}"
        )


def main():

    rclpy.init()

    node = Orders()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()