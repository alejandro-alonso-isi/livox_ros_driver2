import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import json

# Definições das variáveis
host_ip = "192.168.1.5"

## Config HAP
cmd_data_port_HAP = 56000
push_msg_port_HAP = 0
point_data_port_HAP = 57000
imu_data_port_HAP = 58000
log_data_port_HAP = 59000

## Config MID360
cmd_data_port_MID360 = 56100
push_msg_port_MID360 = 56200
point_data_port_MID360 = 56300
imu_data_port_MID360 = 56400
log_data_port_MID360 = 56500

default_extrinsics_hap = {
    "roll": 0.0,
    "pitch": 0.0,
    "yaw": 0.0,
    "x": 0,
    "y": 0,
    "z": 0
}
default_extrinsics_front ={
    "roll": 0.0,
    "pitch": 0.0,
    "yaw": 0.0,
    "x": 0,
    "y": 0,
    "z": 0
}
default_extrinsics_rear = {
    "roll": 0.0,
    "pitch": 0.0,
    "yaw": 0.0,
    "x": 0,
    "y": 0,
    "z": 0
}


format_config = {
    "lidar_summary_info": {
        "lidar_type": 8
    },
    "HAP": {
        "lidar_net_info": {
            "cmd_data_port": cmd_data_port_HAP,
            "push_msg_port": push_msg_port_HAP,
            "point_data_port": point_data_port_HAP,
            "imu_data_port": imu_data_port_HAP,
            "log_data_port": log_data_port_HAP
        },
        "host_net_info": {
            "cmd_data_ip": host_ip,
            "cmd_data_port": cmd_data_port_HAP,
            "push_msg_ip": "",
            "push_msg_port": push_msg_port_HAP,
            "point_data_ip": host_ip,
            "point_data_port": point_data_port_HAP,
            "imu_data_ip": host_ip,
            "imu_data_port": imu_data_port_HAP,
            "log_data_ip": "",
            "log_data_port": log_data_port_HAP
        }
    },
    "MID360": {
        "lidar_net_info": {
            "cmd_data_port": cmd_data_port_MID360,
            "push_msg_port": push_msg_port_MID360,
            "point_data_port": point_data_port_MID360,
            "imu_data_port": imu_data_port_MID360,
            "log_data_port": log_data_port_MID360
        },
        "host_net_info": {
            "cmd_data_ip": host_ip,
            "cmd_data_port": cmd_data_port_MID360,
            "push_msg_ip": host_ip,
            "push_msg_port": push_msg_port_MID360,
            "point_data_ip": host_ip,
            "point_data_port": point_data_port_MID360,
            "imu_data_ip": host_ip,
            "imu_data_port": imu_data_port_MID360,
            "log_data_ip": "",
            "log_data_port": log_data_port_MID360
        }
    },
    "lidar_configs": [
        {
            "ip": "192.168.1.100",
            "pcl_data_type": "{{pcl_data_type_default}}",
            "pattern_mode": "{{pattern_mode_default}}",
            "extrinsic_parameter": "{{default_extrinsics_hap}}"
        },
        {
            "ip": "192.168.1.125",
            "pcl_data_type": "{{pcl_data_type_default}}",
            "pattern_mode": "{{pattern_mode_default}}",
            "extrinsic_parameter": "{{default_extrinsics_front}}"
        },
        {   
            "ip": "192.168.1.128",
            "pcl_data_type": "{{pcl_data_type_default}}",
            "pattern_mode": "{{pattern_mode_default}}",
            "extrinsic_parameter": "{{default_extrinsics_rear}}"
          }
      ]
}

cur_path = os.path.split(os.path.realpath(__file__))[0] + '/'
cur_config_path = cur_path + '../config'
user_config_path = os.path.join(cur_config_path, 'final_config.json')

# Verifica se o arquivo já existe
if not os.path.exists(user_config_path):
    with open(user_config_path, 'w') as json_file:
        json.dump(format_config, json_file, indent=2)
    # print(f"Arquivo salvo em: {user_config_path}")

def generate_launch_description():
    DeclareLaunchArgument('xfer_format', default_value='0', description='Transfer format (0-Pointcloud2, 1-customized)')
    DeclareLaunchArgument('multi_topic', default_value='0', description='Multi-topic configuration (0-All LiDARs share same topic, 1-One LiDAR one topic)')
    DeclareLaunchArgument('data_src', default_value='0', description='Data source configuration (0-lidar, others-invalid)')
    DeclareLaunchArgument('publish_freq', default_value='10.0', description='Publish frequency')
    DeclareLaunchArgument('output_type', default_value='0', description='Output type')
    DeclareLaunchArgument('frame_id', default_value='livox_frame', description='Frame ID')
    DeclareLaunchArgument('lvx_file_path', default_value='/home/livox/livox_test.lvx', description='Path to LVX file')
    DeclareLaunchArgument('cmdline_bd_code', default_value='livox0000000001', description='Command line board code')
    DeclareLaunchArgument('user_config_path', default_value=user_config_path, description='Path to the user config file')
    
    livox_driver = Node(
        package='livox_ros_driver2',
        executable='livox_ros_driver2_node',
        name='livox_lidar_publisher',
        output='screen',
        parameters= [
            {"xfer_format": LaunchConfiguration('xfer_format')},
            {"multi_topic": LaunchConfiguration('multi_topic')},
            {"data_src": LaunchConfiguration('data_src')},
            {"publish_freq": LaunchConfiguration('publish_freq')},
            {"output_data_type": LaunchConfiguration('output_type')},
            {"frame_id": LaunchConfiguration('frame_id')},
            {"lvx_file_path": LaunchConfiguration('lvx_file_path')},
            {"cmdline_input_bd_code": LaunchConfiguration('cmdline_bd_code')},
            {"user_config_path": LaunchConfiguration('user_config_path')}
        ]
        )
    return LaunchDescription([
    livox_driver
])

