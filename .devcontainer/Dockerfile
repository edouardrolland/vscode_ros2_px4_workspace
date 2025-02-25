# Use the base ROS 2 image with the specified tag
# Change this to run the latest version of PX4
FROM kaspergrontved/px4:v1.14

# ** [Optional] Uncomment this section to install additional packages. **
#
# ENV DEBIAN_FRONTEND=noninteractive
# RUN apt-get update \
#    && apt-get -y install --no-install-recommends <your-package-list-here> \
#    #
#    # Clean up
#    && apt-get autoremove -y \
#    && apt-get clean -y \
#    && rm -rf /var/lib/apt/lists/*
# ENV DEBIAN_FRONTEND=dialog

# Add an environment variable for the workspace
ARG WORKSPACE
RUN echo "if [ -f ${WORKSPACE}/install/setup.bash ]; then source ${WORKSPACE}/install/setup.bash; fi" >> /home/ros/.bashrc
RUN echo "source /home/ros/ws_sensor_combined/install/setup.bash" >> /home/ros/.bashrc

RUN /bin/bash -c "sudo chown -R $USER:$USER /home/$USER/PX4-Autopilot"