FROM ros:humble-ros-base

RUN apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ws

COPY src /ws/src
COPY launch /ws/src/launch

RUN . /opt/ros/humble/setup.sh && \
    colcon build --symlink-install

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
