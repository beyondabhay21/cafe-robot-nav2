import yaml

class Points:

    def __init__(self):

        with open(
            "/root/ros2_ws/src/cafe_robot/config/points.yaml",
            "r"
        ) as file:

            self.points = yaml.safe_load(file)

    def get(self, name):

        return self.points[name]