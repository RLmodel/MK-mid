#!/usr/bin/env python3

# Author: Brighten Lee

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time", default="false")
    slam_config_dir = LaunchConfiguration(
        "slam_config_dir",
        default=os.path.join(
            get_package_share_directory("mk_mid_bringup"),
            "config",
            "slam.yaml",
        ),
    )

    rviz_config_dir = os.path.join(get_package_share_directory('mk_mid_bringup'),
                                   'rviz', 'slam_toolbox_default.rviz')
    

    return LaunchDescription(
        [
            Node(
                package="slam_toolbox",
                # executable="lifelong_slam_toolbox_node", 
                executable="async_slam_toolbox_node",
                name="slam_toolbox",
                output="screen",
                parameters=[slam_config_dir, {"use_sim_time": use_sim_time}],
            ),
            
            Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'),


        ]
    )
