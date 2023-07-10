from launch.actions import RegisterEventHandler, EmitEvent
from launch.event_handlers import OnProcessExit
from launch.events import Shutdown


from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

from ament_index_python.packages import get_package_share_directory
from pathlib import Path

from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import SetEnvironmentVariable


ignition_ros_package_path = get_package_share_directory('ros_gz_sim')
udemy_ros2_pkg_path= get_package_share_directory("udemy_ros2_pkg")
simulation_world_file_path=Path(udemy_ros2_pkg_path,"worlds/simulation_project_world.sdf").as_posix()
simulation_models_path=Path(udemy_ros2_pkg_path,"models").as_posix()


simulation=ExecuteProcess(
    cmd=['ign', 'gazebo', '-r', simulation_world_file_path],
    output="screen"
)


def generate_launch_description():
    return LaunchDescription([
        # IncludeLaunchDescription(
        # PythonLaunchDescriptionSource(
        # launch_file_path=Path(ignition_ros_package_path,"launch/gz_sim.launch.py").as_posix()
        # ),
        # launch_arguments={"gz_args": "-r" + simulation_world_file_path}.items()
        # ),

        SetEnvironmentVariable(
            name="IGN_GAZEBO_RESOURCE_PATH",
            value=simulation_models_path
        ),
        simulation,

        Node(
        package="ros_ign_bridge",
        executable="parameter_bridge",
        arguments=["/cmd_vel@geometry_msgs/msg/Twist@ignition.msgs.Twist",
                   "/camera@sensor_msgs/msg/Image@ignition.msgs.Image",
                   "camera_rod_pos_cmd@std_msgs/msg/Float64@ignition.msgs.Double",
        ],
        remappings=[
            ("/camera", "/camera/image_raw")
        ],
      
        output="screen"
        ),
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=simulation,
                on_exit=[EmitEvent(event=Shutdown())],
            )
        )
    ])