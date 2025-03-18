import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import os

def generate_launch_description():
    pkgpath = launch_ros.substitutions.FindPackageShare(package='urdf_humble_test').find('urdf_humble_test')
    urdfModelPath = os.path.join(pkgpath, 'urdf/model.urdf')
    rvizConfigPath = os.path.join(pkgpath, 'config/config.rviz')

    print(urdfModelPath)
    with open(urdfModelPath, 'r') as file:
        rocot_desc = file.read()

    params = {'robot_description': rocot_desc}

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[params],
        arguments=[urdfModelPath]
    )

    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[params],
        arguments=[urdfModelPath]
    )

    joint_state_publisher_gui_node = launch_ros.actions.Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        arguments=[urdfModelPath],
        condition=launch.conditions.IfCondition(LaunchConfiguration('gui'))
    )

    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rvizConfigPath],
    )

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='gui', default_value='True', description='This is a flag for joint_state_publisher_gui'),
        robot_state_publisher_node,
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])
