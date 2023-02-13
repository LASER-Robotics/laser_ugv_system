from ament_index_python.packages import get_package_share_path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

def generate_launch_description():
    ugv_simulation_path = get_package_share_path("ugv_simulation")
    world_gazebo_path = ugv_simulation_path / "worlds/laser.world"
    
    world_gazebo_arg = DeclareLaunchArgument(name="world", default_value=str(world_gazebo_path), description="World for spawnner oni claw")
    
    gazebo_launch = ExecuteProcess(
        cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so',  '-s', 'libgazebo_ros_init.so', LaunchConfiguration('world')],
        output='screen'
    )

    return LaunchDescription([
        world_gazebo_arg ,
        gazebo_launch ,
    ]) 