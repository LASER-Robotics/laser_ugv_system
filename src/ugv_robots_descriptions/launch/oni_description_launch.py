from ament_index_python.packages import get_package_share_path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition

from launch_ros.actions import Node


def generate_launch_description():
    ugv_robots_description_path = get_package_share_path("ugv_robots_description")
    model_oni_path = ugv_robots_description_path / "robots_description/oni.urdf.xacro"
    rviz_config_path = ugv_robots_description_path / "rviz/rviz_minimal_visualization_config.rviz"

    gui_arg = DeclareLaunchArgument(name="gui_joint", default_value="false", choices=["true", "false"], description="Flag to enable joint_state_publisher_gui")
    model_arg = DeclareLaunchArgument(name="model", default_value=str(model_oni_path), description="Absolute path to robot urdf file")
    rviz_config_arg = DeclareLaunchArgument(name="rvizconfig", default_value=str(rviz_config_path), description="Absolute path to rviz config file")
    rviz_launch_arg = DeclareLaunchArgument(name="rviz", default_value="true", choices=["true", "false"], description="Launch rviz with basic visualization of robot")
    use_sim_time_arg = DeclareLaunchArgument(name="use_sim_time", default_value="true", choices=["true", "false"], description='Flag to enable use_sim_time')
    
    robot_state_publisher_node = Node(
   	 	package= "robot_state_publisher" ,
   	 	executable= "robot_state_publisher" ,
   	 	name= "robot_state_publisher" ,
   	 	parameters= [{"robot_description" : Command(["xacro ", LaunchConfiguration("model")])}]
    )
 
    joint_state_publisher_node = Node(
   		package="joint_state_publisher",
   		executable="joint_state_publisher",
   		name="joint_state_publisher_node" ,
     	condition=UnlessCondition(LaunchConfiguration("gui_joint"))
   	 )

    joint_state_publisher_gui_node = Node(
   		package="joint_state_publisher_gui",
   		executable="joint_state_publisher_gui",
		name="joint_state_publisher_node_gui" ,
  		condition=IfCondition(LaunchConfiguration("gui_joint"))
   	 )
    
    robot_localization_node = Node(
		package="robot_localization" ,
		executable="ekf_node" ,
		name="ekf_filter_node" ,
		output="screen" ,
		parameters=[str(get_package_share_path("ugv_simulation") / "config/ekf_oni.yaml"), {"use_sim_time" : LaunchConfiguration("use_sim_time")}] 
	)
    
    rviz_node = Node(
   	 	package= "rviz2" ,
   	 	executable= "rviz2" ,
   	 	name= "rviz2" ,
   	 	output= "screen" ,
   	 	arguments=["-d", LaunchConfiguration("rvizconfig")] ,
		condition=IfCondition(LaunchConfiguration("rviz"))
    )
    
    gazebo_node = Node(
   	 	package= "gazebo_ros",
   	 	executable= "spawn_entity.py" ,
   	 	name= "oni_spawner" ,
   	 	output= "screen" ,
   	 	arguments= ["-topic", "/robot_description", "-entity", "oni", "-z", "0.03"]
    )

    return LaunchDescription([
   	 	gui_arg,
    	model_arg ,
   	 	rviz_config_arg ,
		rviz_launch_arg ,
  		use_sim_time_arg ,
   	 	joint_state_publisher_node ,
   	 	joint_state_publisher_gui_node ,
      	robot_state_publisher_node ,
		robot_localization_node ,
		gazebo_node ,
   	 	rviz_node ,	
    ])