from enum import Enum


class RobotState(Enum):

    IDLE = "idle"

    TO_KITCHEN = "to_kitchen"

    WAIT_KITCHEN = "wait_kitchen"

    TO_TABLE = "to_table"

    WAIT_TABLE = "wait_table"

    BACK_KITCHEN = "back_kitchen"

    BACK_HOME = "back_home"

    CANCELLED = "cancelled"