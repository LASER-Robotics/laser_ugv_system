from launch import LaunchDescription

def generate_launch_description():
     included_launch = IncludeLaunchDescription(package='foo', launch='my_launch.py', arguments=[...])  