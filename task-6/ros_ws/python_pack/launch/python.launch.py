import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    # Path to parameter file
    pkg_share = get_package_share_directory('python_pack')
    params_file = os.path.join(pkg_share, 'config', 'params.yaml')

    # 1. Turtlesim Node
    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim_node',
        output='screen'
    )

    # 2. Go To Goal Node (Service Server, loaded with its parameter file)
    go_to_goal_node = Node(
        package='python_pack',
        executable='go_to_goal_node',
        name='go_to_goal_node',
        output='screen',
        parameters=[params_file]
    )

    # 3. Service Client Node
    client_node = Node(
        package='python_pack',
        executable='client',
        name='client',
        output='screen'
    )

    return LaunchDescription([
        turtlesim_node,
        go_to_goal_node,
        client_node
    ])