FROM beasley_weather_base:latest


RUN pip3 install pexpect


# Install weewx
RUN wget -qO - http://weewx.com/keys.html | apt-key add - && \
    wget -qO - http://weewx.com/apt/weewx.list | tee /etc/apt/sources.list.d/weewx.list
COPY ./docker/install_weewx.py .
RUN python3 install_weewx.py
RUN rm install_weewx.py

# Config
COPY ./docker/weewx.conf /etc/weewx/


# Clean up
RUN pip uninstall -y pexpect


ENTRYPOINT ["weewxd", "/etc/weewx/weewx.conf"]
