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
    use_sim_time_arg = DeclareLaunchArgument(name="use_sim_time", default_value="true", choices=["true", "false"], description='Flag to enable use_sim_time')
    
    gazebo_launch = ExecuteProcess(
        cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so',  '-s', 'libgazebo_ros_init.so', LaunchConfiguration('world')],
        output='screen'
    )
    
    robot_localization_node = Node(
        package="robot_localization" ,
        executable="ekf_node" ,
        name="ekf_filter_node" ,
        output="screen" ,
        parameters=[str(ugv_simulation_path / "config/ekf_oni.yaml"), {"use_sim_time" : LaunchConfiguration("use_sim_time")}] 
    )
    
    return LaunchDescription([
        world_gazebo_arg ,
        use_sim_time_arg ,
        gazebo_launch ,
        robot_localization_node ,
    ]) 