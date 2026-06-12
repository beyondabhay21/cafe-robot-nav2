import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_msgs.msg import Bool

from cafe_robot.robot_states import RobotState


class MainRobot(Node):

    def __init__(self):

        super().__init__("main_robot")

        self.state = RobotState.IDLE

        self.orders = []

        self.cancelled = False

        self.kitchen_confirmed = False

        self.table_confirmed = False

        # Order subscriber
        self.create_subscription(
            String,
            "/order",
            self.order_callback,
            10
        )

        # Confirmation subscriber
        self.create_subscription(
            Bool,
            "/confirm",
            self.confirm_callback,
            10
        )

        # Cancel subscriber
        self.create_subscription(
            Bool,
            "/cancel",
            self.cancel_callback,
            10
        )

        self.get_logger().info(
            "Cafe Robot Ready"
        )

    # -------------------------
    # Callbacks
    # -------------------------

    def order_callback(self, msg):

        table = msg.data

        self.orders.append(table)

        self.get_logger().info(
            f"Order received for {table}"
        )

        self.run_delivery(table)

    def confirm_callback(self, msg):

        if self.state == RobotState.WAIT_KITCHEN:

            self.kitchen_confirmed = msg.data

            self.get_logger().info(
                "Kitchen confirmed"
            )

        elif self.state == RobotState.WAIT_TABLE:

            self.table_confirmed = msg.data

            self.get_logger().info(
                "Table confirmed"
            )

    def cancel_callback(self, msg):

        self.cancelled = msg.data

        if self.cancelled:

            self.get_logger().warn(
                "Order cancelled"
            )

    # -------------------------
    # Delivery Logic
    # -------------------------

    def run_delivery(self, table):

        self.cancelled = False

        self.kitchen_confirmed = False

        self.table_confirmed = False

        # Home -> Kitchen

        self.state = RobotState.TO_KITCHEN

        self.get_logger().info(
            "Going to kitchen"
        )

        self.get_logger().info(
            "Reached kitchen"
        )

        # Wait Kitchen

        self.state = RobotState.WAIT_KITCHEN

        self.get_logger().info(
            "Waiting for kitchen confirmation"
        )

        # For now simulate confirmation

        self.kitchen_confirmed = True

        if not self.kitchen_confirmed:

            self.get_logger().warn(
                "Kitchen timeout"
            )

            self.return_home()

            return

        # Kitchen -> Table

        self.state = RobotState.TO_TABLE

        self.get_logger().info(
            f"Going to {table}"
        )

        self.get_logger().info(
            f"Reached {table}"
        )

        # Wait Table

        self.state = RobotState.WAIT_TABLE

        self.get_logger().info(
            "Waiting for table confirmation"
        )

        # For now simulate confirmation

        self.table_confirmed = True

        if not self.table_confirmed:

            self.get_logger().warn(
                "Table timeout"
            )

            self.return_kitchen()

            self.return_home()

            return

        # Check cancellation

        if self.cancelled:

            self.return_home()

            return

        # Return Home

        self.return_home()

    # -------------------------
    # Helpers
    # -------------------------

    def return_kitchen(self):

        self.state = RobotState.BACK_KITCHEN

        self.get_logger().info(
            "Returning to kitchen"
        )

    def return_home(self):

        self.state = RobotState.BACK_HOME

        self.get_logger().info(
            "Returning home"
        )

        self.state = RobotState.IDLE

        self.get_logger().info(
            "Task complete"
        )


def main():

    rclpy.init()

    node = MainRobot()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()