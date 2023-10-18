FROM althack/ros2:humble-full

RUN apt-get update && \
    apt-get install -y git && \
    git clone https://github.com/PX4/PX4-Autopilot.git --recursive /home/ros/PX4-Autopilot && \
    bash /home/ros/PX4-Autopilot/Tools/setup/ubuntu.sh && \
    cd /home/ros/PX4-Autopilot/ && \
    make px4_sitl

RUN apt-get install -y python3-pip && \
    pip3 install -U empy pyros-genmsg setuptools

RUN git clone https://github.com/eProsima/Micro-XRCE-DDS-Agent.git /home/ros/Micro-XRCE-DDS-Agent && \
    cd /home/ros/Micro-XRCE-DDS-Agent && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install && \
    ldconfig /usr/local/lib/

# [Optional] Uncomment this section to install additional packages.
# ENV DEBIAN_FRONTEND=noninteractive
# RUN apt-get update \
#    && apt-get -y install --no-install-recommends <your-package-list-here> \
#    #
#    # Clean up
#    && apt-get autoremove -y \
#    && apt-get clean -y \
#    && rm -rf /var/lib/apt/lists/*
# ENV DEBIAN_FRONTEND=dialog

# Set up auto-source of workspace for ros user
ARG WORKSPACE
RUN echo "if [ -f ${WORKSPACE}/install/setup.bash ]; then source ${WORKSPACE}/install/setup.bash; fi" >> /home/ros/.bashrc
