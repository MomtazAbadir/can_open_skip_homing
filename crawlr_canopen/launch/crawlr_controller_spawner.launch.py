import os
import launch_ros
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
import launch
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import TextSubstitution, LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Load the controllers from the YAML configuration
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )

    # Spawning the velocity controller from the YAML config
    leg_velocity_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["leg_velocity_controller", "--controller-manager", "/controller_manager"],
    )

    # Spawning the wheel_controller from the YAML config
    wheel_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["wheel_controller", "--controller-manager", "/controller_manager"],
    )
    
        # Spawning the leg_position_controller from the YAML config
    leg_position_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["leg_position_controller", "--controller-manager", "/controller_manager"],
    )
    
 
    return LaunchDescription(
        [
            joint_state_broadcaster_spawner,
            leg_position_controller_spawner,
            wheel_controller_spawner,
        ],
    )

