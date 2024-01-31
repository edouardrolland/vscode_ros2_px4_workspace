# Use the base ROS 2 image with the specified tag
FROM althack/ros2:humble-full

# Update packages and install git
RUN apt-get update && \
    apt-get install -y git python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Clone PX4-Autopilot repository and build
RUN git clone --recursive https://github.com/PX4/PX4-Autopilot.git /home/ros/PX4-Autopilot && \
    bash /home/ros/PX4-Autopilot/Tools/setup/ubuntu.sh && \
    cd /home/ros/PX4-Autopilot/ && \
    make px4_sitl

# Install Python dependencies
RUN pip3 install -U empy==3.3.4 pyros-genmsg setuptools

# Clone and build Micro-XRCE-DDS-Agent
RUN git clone https://github.com/eProsima/Micro-XRCE-DDS-Agent.git /home/ros/Micro-XRCE-DDS-Agent && \
    cd /home/ros/Micro-XRCE-DDS-Agent && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install && \
    ldconfig /usr/local/lib/

# Clone PX4 repositories
RUN mkdir -p /home/ros/ws_sensor_combined/src/ && \
   git clone https://github.com/PX4/px4_msgs.git /home/ros/ws_sensor_combined/src/px4_msgs && \
   git clone https://github.com/PX4/px4_ros_com.git /home/ros/ws_sensor_combined/src/px4_ros_com

# Build the workspace using colcon
RUN cd /home/ros/ws_sensor_combined && \
    /bin/bash -c "source /opt/ros/humble/setup.sh && colcon build"
