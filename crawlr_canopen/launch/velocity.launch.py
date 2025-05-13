import os
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import launch_ros


def generate_launch_description():
    declared_arguments = [
        DeclareLaunchArgument(
            "description_package",
            default_value="crawlr_description",
            description="Package where URDF file is stored.",
        ),
        DeclareLaunchArgument(
            "can_interface",
            default_value="can0",
            description="Interface name for CAN.",
        ),
        DeclareLaunchArgument(
            "use_ros2_control",
            default_value="true",
            description="Use ros2_control.",
        ),
    ]

    can_interface = LaunchConfiguration("can_interface")

    controller_config = PathJoinSubstitution([
        FindPackageShare("crawlr_canopen"), "config", "ros2_controllers_velocity.yaml"
    ])
    bus_config = PathJoinSubstitution([
        FindPackageShare("crawlr_canopen"), "config", "velocity", "bus.yml"
    ])
    master_config = PathJoinSubstitution([
        FindPackageShare("crawlr_canopen"), "config", "velocity", "master.dcf"
    ])

    robot_description_content = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]), " ",
        PathJoinSubstitution([
            FindPackageShare(LaunchConfiguration("description_package")),
            "urdf", "crawlr.xacro"
        ]),
        " ",
        "bus_config:=", bus_config,
        " ",
        "master_config:=", master_config,
        " ",
        "can_interface:=", can_interface,
    ])

    robot_description = {
        "robot_description": launch_ros.descriptions.ParameterValue(
            robot_description_content, value_type=str
        )
    }

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )

    controller_manager_node = TimerAction(
        period=2.0,
        actions=[
            Node(
                package="controller_manager",
                executable="ros2_control_node",
                output="both",
                parameters=[robot_description, controller_config],
            )
        ]
    )

    controller_spawner_node = TimerAction(
        period=3.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(PathJoinSubstitution([
                    FindPackageShare("crawlr_canopen"),
                    "launch",
                    "crawlr_controller_spawner.launch.py"
                ])),
                launch_arguments={}.items(),
            )
        ]
    )

    return LaunchDescription(declared_arguments + [
        robot_state_publisher_node,
        controller_manager_node,
        controller_spawner_node,
    ])

