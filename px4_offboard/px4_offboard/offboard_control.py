#!/usr/bin/env python

import rclpy
import numpy as np
from rclpy.node import Node
from rclpy.clock import Clock
from rclpy.qos import (
    QoSProfile,
    QoSReliabilityPolicy,
    QoSHistoryPolicy,
    QoSDurabilityPolicy,
)

from px4_msgs.msg import OffboardControlMode
from px4_msgs.msg import TrajectorySetpoint
from px4_msgs.msg import VehicleCommand
from px4_msgs.msg import VehicleStatus


class OffboardControl(Node):
    def __init__(self):
        super().__init__("offboard_control")
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT,
            durability=QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL,
            history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST,
            depth=1,
        )

        self.status_sub = self.create_subscription(
            VehicleStatus,
            "/fmu/out/vehicle_status",
            self.vehicle_status_callback,
            qos_profile,
        )
        self.publisher_offboard_mode = self.create_publisher(
            OffboardControlMode, "/fmu/in/offboard_control_mode", qos_profile
        )
        self.publisher_trajectory = self.create_publisher(
            TrajectorySetpoint, "/fmu/in/trajectory_setpoint", qos_profile
        )
        self.vehicle_command_publisher = self.create_publisher(
            VehicleCommand, "/fmu/in/vehicle_command", qos_profile
        )
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.cmdloop_callback)

        self.nav_state = VehicleStatus.NAVIGATION_STATE_MAX
        self.dt = timer_period
        self.theta = 0.0
        self.theta2 = 0.0
        self.radius = 10.0
        self.omega = 0.3
        self.arming_state = 0.0

        self.counter = 0

    def arm(self):
        self.publish_vehicle_command(
            VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM,
            VehicleCommand.ARMING_ACTION_ARM,
        )
        self.get_logger().info("Arming vehicle!")

    def disarm(self):
        self.publish_vehicle_command(
            VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM,
            VehicleCommand.ARMING_ACTION_DISARM,
        )
        self.get_logger().info("Disarming vehicle!")

    """
	Publish vehicle commands
	command   Command code (matches VehicleCommand and MAVLink MAV_CMD codes)
	param1    Command parameter 1
                VEHICLE_MODE_FLAG_CUSTOM_MODE_ENABLED = 1
	            VEHICLE_MODE_FLAG_TEST_ENABLED = 2, /* 0b00000010 system has a test mode enabled. This flag is intended for temporary system tests and should not be used for stable implementations. | */
	            VEHICLE_MODE_FLAG_AUTO_ENABLED = 4, /* 0b00000100 autonomous mode enabled, system finds its own goal positions. Guided flag can be set or not, depends on the actual implementation. | */
	            VEHICLE_MODE_FLAG_GUIDED_ENABLED = 8, /* 0b00001000 guided mode enabled, system flies MISSIONs / mission items. | */
	            VEHICLE_MODE_FLAG_STABILIZE_ENABLED = 16, /* 0b00010000 system stabilizes electronically its attitude (and optionally position). It needs however further control inputs to move around. | */
	            VEHICLE_MODE_FLAG_HIL_ENABLED = 32, /* 0b00100000 hardware in the loop simulation. All motors / actuators are blocked, but internal software is full operational. | */
	            VEHICLE_MODE_FLAG_MANUAL_INPUT_ENABLED = 64, /* 0b01000000 remote control input is enabled. | */
	param2    Command parameter 2
                PX4_CUSTOM_MAIN_MODE_MANUAL = 1,
	            PX4_CUSTOM_MAIN_MODE_ALTCTL = 2,
	            PX4_CUSTOM_MAIN_MODE_POSCTL = 3,
	            PX4_CUSTOM_MAIN_MODE_AUTO = 4,
	            PX4_CUSTOM_MAIN_MODE_ACRO = 5,
	            PX4_CUSTOM_MAIN_MODE_OFFBOARD = 6,
	            PX4_CUSTOM_MAIN_MODE_STABILIZED = 7,
	            PX4_CUSTOM_MAIN_MODE_RATTITUDE_LEGACY = 8
    """

    def publish_vehicle_command(self, command, param1=0.0, param2=0.0):
        msg = VehicleCommand()
        msg.timestamp = int(Clock().now().nanoseconds / 1000)
        msg.param1 = float(param1)
        msg.param2 = float(param2)
        msg.command = command
        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        msg.from_external = True
        self.vehicle_command_publisher.publish(msg=msg)

    # Change mode to offboard and arm vehicle
    # This mode requires position or pose/attitude information - e.g. GPS, optical flow, visual-inertial odometry, mocap, etc.
    # RC control is disabled except to change modes.
    # The vehicle must be armed before this mode can be engaged.
    # The vehicle must be already be receiving a stream of target setpoints (>2Hz) before this mode can be engaged.
    # The vehicle will exit the mode if target setpoints are not received at a rate of > 2Hz.
    # Not all coordinate frames and field values allowed by MAVLink are supported.
    
    def set_mode_offboard(self):

        self.get_logger().info("Setting mode to offboard!")
        self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_DO_SET_MODE, 1.0, 6.0)

    def vehicle_status_callback(self, msg):
        self.arming_state = msg.arming_state
        self.nav_state = msg.nav_state

    def publish_offboard_control_mode(self):
        offboard_msg = OffboardControlMode()
        offboard_msg.timestamp = int(Clock().now().nanoseconds / 1000)
        offboard_msg.position = True
        offboard_msg.velocity = False
        offboard_msg.acceleration = False
        self.publisher_offboard_mode.publish(offboard_msg)

    def publish_trajectory_setpoint(self):
        trajectory_msg = TrajectorySetpoint()
        trajectory_msg.position[0] = self.radius * np.cos(self.theta)
        trajectory_msg.position[1] = self.radius * np.sin(self.theta2)
        trajectory_msg.position[2] = -np.abs(self.radius * np.sin(self.theta2))
        trajectory_msg.yaw =np.arctan2(np.sin(self.theta), np.cos(self.theta2)) +np.pi/2
        self.publisher_trajectory.publish(trajectory_msg)
        self.theta = self.theta + self.omega * self.dt
        self.theta2 = self.theta2 + self.omega * 2 * self.dt

    def cmdloop_callback(self):
        # Publish offboard control modes
        self.publish_offboard_control_mode()
        if self.arming_state == 0.0:
            self.arm()
            self.set_mode_offboard()
        elif self.nav_state == VehicleStatus.NAVIGATION_STATE_OFFBOARD:
            self.publish_trajectory_setpoint()


def main(args=None):
    rclpy.init(args=args)

    offboard_control = OffboardControl()

    rclpy.spin(offboard_control)

    offboard_control.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()