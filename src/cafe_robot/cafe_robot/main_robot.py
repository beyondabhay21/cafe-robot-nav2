import rclpy

from rclpy.node import Node

from std_msgs.msg import String

from cafe_robot.robot_states import RobotState


class MainRobot(Node):

    def __init__(self):

        super().__init__("main_robot")

        self.state = RobotState.IDLE

        self.create_subscription(
            String,
            "/order",
            self.order_callback,
            10
        )

        self.get_logger().info(
            "Cafe Robot Ready"
        )

    def order_callback(self, msg):

        table = msg.data

        self.get_logger().info(
            f"Order received for {table}"
        )

        self.run_delivery(table)

    def run_delivery(self, table):

        self.state = RobotState.TO_KITCHEN

        self.get_logger().info(
            "Going to kitchen"
        )

        self.state = RobotState.TO_TABLE

        self.get_logger().info(
            f"Delivering to {table}"
        )

        self.state = RobotState.BACK_HOME

        self.get_logger().info(
            "Returning home"
        )

        self.state = RobotState.IDLE

        self.get_logger().info(
            "Task Complete"
        )

    def scenario1(self, table):

        self.get_logger().info("Going to kitchen")

        self.get_logger().info(
            f"Delivering to {table}"
        )

        self.get_logger().info(
            "Returning home"
        )


def main():

    rclpy.init()

    node = MainRobot()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()