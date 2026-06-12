from enum import Enum


class RobotState(Enum):

    IDLE = "idle"

    TO_KITCHEN = "to_kitchen"

    TO_TABLE = "to_table"

    BACK_HOME = "back_home"