import time

import rclpy
from rclpy.node import Node
import threading
from std_msgs.msg import String
from std_msgs.msg import Bool

from cafe_robot.robot_states import RobotState
from cafe_robot.order_queue import OrderQueue


class MainRobot(Node):

    def __init__(self):

        super().__init__("main_robot")

        self.state = RobotState.IDLE

        self.queue = OrderQueue()

        self.processing = False

        self.cancelled = False

        self.kitchen_confirmed = False

        self.table_confirmed = False

        self.create_subscription(
            String,
            "/order",
            self.order_callback,
            10
        )

        self.create_subscription(
            Bool,
            "/confirm",
            self.confirm_callback,
            10
        )

        self.create_subscription(
            Bool,
            "/cancel",
            self.cancel_callback,
            10
        )

        self.get_logger().info(
            "Cafe Robot Ready"
        )

    # ----------------------------------
    # Callbacks
    # ----------------------------------

    def order_callback(self, msg):

        table = msg.data

        self.queue.add(table)

        self.get_logger().info(
            f"Order received for {table}"
        )

        if self.state == RobotState.IDLE:

            threading.Thread(
                target=self.process_orders,
                daemon=True
            ).start()

    def confirm_callback(self, msg):

        self.get_logger().info(
            f"Confirm received: {msg.data}"
        )

        if self.state == RobotState.WAIT_KITCHEN:

            self.kitchen_confirmed = msg.data

            self.get_logger().info(
                "Kitchen confirmation accepted"
            )

        elif self.state == RobotState.WAIT_TABLE:

            self.table_confirmed = msg.data

            self.get_logger().info(
                "Table confirmation accepted"
            )

        else:

            self.get_logger().warn(
                f"Confirmation ignored. Current state: {self.state.value}"
            )

    def cancel_callback(self, msg):

        self.cancelled = msg.data

        if self.cancelled:

            self.get_logger().warn(
                "Order cancelled"
            )

    # ----------------------------------
    # Order Processing
    # ----------------------------------

    def process_orders(self):

        if self.processing:
            return

        self.processing = True

        while not self.queue.empty():

            table = self.queue.next_order()

            self.run_delivery(table)

        self.processing = False

    # ----------------------------------
    # Delivery Logic
    # ----------------------------------

    def run_delivery(self, table):

        self.cancelled = False

        self.kitchen_confirmed = False

        self.table_confirmed = False

        # -------------------
        # Kitchen
        # -------------------

        self.state = RobotState.TO_KITCHEN

        self.get_logger().info(
            "Going to kitchen"
        )

        self.get_logger().info(
            "Reached kitchen"
        )

        self.state = RobotState.WAIT_KITCHEN

        self.get_logger().info(
            "Waiting for kitchen confirmation"
        )

        if not self.wait_for_kitchen():

            return

        # -------------------
        # Table
        # -------------------

        self.state = RobotState.TO_TABLE

        self.get_logger().info(
            f"Going to {table}"
        )

        self.get_logger().info(
            f"Reached {table}"
        )

        self.state = RobotState.WAIT_TABLE

        self.get_logger().info(
            "Waiting for table confirmation"
        )

        if not self.wait_for_table():

            return

        # -------------------
        # Success
        # -------------------

        self.return_home()

    # ----------------------------------
    # Wait Helpers
    # ----------------------------------

    def wait_for_kitchen(self):

        timeout = 60

        start_time = time.time()

        while not self.kitchen_confirmed:

            if self.cancelled:

                self.return_home()
                return False

            if time.time() - start_time > timeout:

                self.get_logger().warn(
                    "Kitchen timeout"
                )

                self.return_home()

                return False

            rclpy.spin_once(self, timeout_sec=0.1)

        return True

    def wait_for_table(self):

        timeout = 60

        start_time = time.time()

        while not self.table_confirmed:

            if self.cancelled:

                self.return_home()
                return False

            if time.time() - start_time > timeout:

                self.get_logger().warn(
                    "Table timeout"
                )

                self.return_kitchen()

                self.return_home()

                return False

            rclpy.spin_once(self, timeout_sec=0.1)

        return True

    # ----------------------------------
    # Navigation Helpers
    # ----------------------------------

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