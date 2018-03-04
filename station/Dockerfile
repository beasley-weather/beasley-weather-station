FROM ubuntu:xenial

# Set the locale
# RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
#     locale-gen
# ENV LANG en_US.UTF-8
# ENV LANGUAGE en_US:en
# ENV LC_ALL en_US.UTF-8

# Install packages
RUN apt-get update && \
    apt-get -y install wget python python-pip python3 python3-pip
RUN pip3 install pexpect

# Install weewx
RUN wget -qO - http://weewx.com/keys.html | apt-key add - && \
    wget -qO - http://weewx.com/apt/weewx.list | tee /etc/apt/sources.list.d/weewx.list
COPY install_weewx.py .
RUN python3 install_weewx.py
RUN rm install_weewx.py
# COPY weewx.conf /etc/weewx/

# Clean up
# RUN apt -y purge wget python3
# RUN pip uninstall -y pexpect


ENTRYPOINT weewxd "/etc/weewx/weewx.conf"
