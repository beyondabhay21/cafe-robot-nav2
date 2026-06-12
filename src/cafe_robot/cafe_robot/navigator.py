from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped


class MoveRobot:

    def __init__(self):

        self.nav = BasicNavigator()

    def go_to(self, x, y):

        goal = PoseStamped()

        goal.header.frame_id = "map"

        goal.pose.position.x = x
        goal.pose.position.y = y

        goal.pose.orientation.w = 1.0

        self.nav.goToPose(goal)

        while not self.nav.isTaskComplete():
            pass

        return True