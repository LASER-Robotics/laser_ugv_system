from launch import LaunchDescription

from launch_ros.actions import Node

def generate_launch_description():  
    teleop_node = Node(
        package="teleop_twist_keyboard",
        executable="teleop_twist_keyboard",
        arguments=["--ros-args-r", "/cmd_vel:=/diff_cont/cmd_vel_unstamped"],
    )

    return LaunchDescription([
        teleop_node ,
    ])