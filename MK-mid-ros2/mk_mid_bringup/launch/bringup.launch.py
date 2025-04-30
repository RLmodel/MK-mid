
import launch

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

from launch.launch_description_sources import PythonLaunchDescriptionSource

"""Launch a sensor node along with os_cloud and os_"""

from pathlib import Path



def generate_launch_description():


    # MK-mid
    mk_mid_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            get_package_share_directory('yhs_can_control'), '/launch/yhs_can_control.launch.py']
            ),)


    # Ouster OS128

    """
    Generate launch description for running ouster_ros components separately each
    component will run in a separate process).
    """
    ouster_ros_pkg_dir = get_package_share_directory('ouster_ros')
    # use the community_driver_config.yaml by default
    default_params_file = \
        Path(ouster_ros_pkg_dir) / 'config' / 'community_driver_config.yaml'
    params_file = LaunchConfiguration('params_file')
    params_file_arg = DeclareLaunchArgument('params_file',
                                            default_value=str(
                                                default_params_file),
                                            description='name or path to the parameters file to use.')

    driver_launch_file_path = \
        Path(ouster_ros_pkg_dir) / 'launch' / 'driver.launch.py'
    driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([str(driver_launch_file_path)]),
        launch_arguments={
            'params_file': params_file,
            'ouster_ns': '',
            'os_driver_name': 'ouster_driver',
            'viz': 'True',
            'rviz_config': './install/ouster_ros/share/ouster_ros/config/community_driver.rviz'
        }.items()
    )

    laser_frame_node = Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    name='static_transform_publisher',
    arguments = ["0", "0", "0.35", "0", "0", "0", "base_link", "laser_sensor_frame"],
    output="screen")


    # IMU && GNSS receiver
    imu_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            get_package_share_directory('microstrain_inertial_driver'), '/launch/microstrain_launch.py']
            ),)
            
    
    # Description
    desc_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            get_package_share_directory('mk_mid_bringup'), '/launch/description.launch.py']
            ),)


    return LaunchDescription([
        
        # lidar_bringup,
        params_file_arg,
        driver_launch,
        laser_frame_node,

        imu_bringup,

        mk_mid_bringup,  ## this launch must be below the ouster launch !!!!
        # desc_bringup,
        
        
    ])

    
