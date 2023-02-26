from ament_index_python.packages import get_package_share_directory, get_package_share_path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition , UnlessCondition
from launch.substitutions import LaunchConfiguration, Command

from launch_ros.actions import Node


def generate_launch_description():
    ugv_robots_description_path = get_package_share_path("ugv_robots_descriptions")
    model_l1br_path = ugv_robots_description_path / "robots_description/l1br/urdf/l1br.urdf.xacro"
    rviz_config_path = ugv_robots_description_path / "rviz/rviz_minimal_visualization_l1br_config.rviz"

    gui_arg = DeclareLaunchArgument(name="gui_joint", default_value="false", choices=["true", "false"], description="Flag to enable joint_state_publisher_gui")
    model_arg = DeclareLaunchArgument(name="model", default_value=str(model_l1br_path), description="Absolute path to robot urdf file")
    rviz_config_arg = DeclareLaunchArgument(name="rvizconfig", default_value=str(rviz_config_path), description="Absolute path to rviz config file")
    rviz_launch_arg = DeclareLaunchArgument(name="rviz", default_value="true", choices=["true", "false"], description="Launch rviz with basic visualization of robot")
    use_sim_time_arg = DeclareLaunchArgument(name="use_sim_time", default_value="true", choices=["true", "false"], description='Flag to enable use_sim_time')
    

    robot_state_publisher_node = Node(
   	 	package= "robot_state_publisher" ,
   	 	executable= "robot_state_publisher" ,
   	 	name= "robot_state_publisher" ,
		namespace="l1br" ,
   	 	parameters= [{"robot_description" : Command(["xacro ", LaunchConfiguration("model")])}]
    )

    joint_state_publisher_node = Node(
   		package="joint_state_publisher",
   		executable="joint_state_publisher",
        namespace="l1br" ,
   		condition=UnlessCondition(LaunchConfiguration("gui_joint"))
    )

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        namespace="l1br" ,
        condition=IfCondition(LaunchConfiguration("gui_joint"))
    )
    
    gazebo = Node(
        package="gazebo_ros" ,
        executable="spawn_entity.py" ,
        name="spawn_l1br" ,
        namespace="l1br" ,
        output="screen" ,
        arguments= ["-topic", "/l1br/robot_description", "-entity", "l1br"] ,
    )
    
    robot_localization_node = Node(
		package="robot_localization" ,
		executable="ekf_node" ,
		name="ekf_filter_node" ,
		output="screen" ,
		namespace="l1br" ,
		parameters=[str(get_package_share_path("ugv_simulation") / "config/ekf_l1br.yaml"), {"use_sim_time" : LaunchConfiguration("use_sim_time")}] 
	)
    
    rviz = Node(
    	package="rviz2",
    	executable="rviz2",
    	name="rviz2",
        namespace="l1br" ,
    	output="screen",
    	arguments= ["-d", LaunchConfiguration("rvizconfig")],
    )

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        namespace="l1br" ,
        arguments=["diff_cont"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        namespace="l1br" ,
        arguments=["joint_broad"],
    )
    return LaunchDescription([
        model_arg ,
        rviz_config_arg ,
        rviz_launch_arg ,
        use_sim_time_arg ,
        gui_arg, 
        rviz ,
        gazebo ,
        robot_localization_node ,
        diff_drive_spawner ,
        joint_broad_spawner ,
        robot_state_publisher_node ,
        joint_state_publisher_node ,
        joint_state_publisher_gui_node ,
    ])
