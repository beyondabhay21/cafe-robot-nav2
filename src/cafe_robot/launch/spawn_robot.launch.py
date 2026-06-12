from launch import LaunchDescription
from launch.actions import ExecuteProcess


def generate_launch_description():

    spawn_robot = ExecuteProcess(

        cmd=[

            'ros2',
            'run',
            'gazebo_ros',
            'spawn_entity.py',

            '-entity',
            'turtlebot3',

            '-topic',
            'robot_description',

            '-x',
            '0',

            '-y',
            '0',

            '-z',
            '0.01'
        ],

        output='screen'
    )

    return LaunchDescription([

        spawn_robot

    ])