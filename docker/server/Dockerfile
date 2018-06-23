FROM beasley_weather_base:latest


ENV WEEWX_DATABASE="/var/lib/weewx/weewx.sdb"
ENV DTS_PORT=24242


RUN pip3 install pexpect


# Install weewx
RUN wget -qO - http://weewx.com/keys.html | apt-key add - && \
    wget -qO - http://weewx.com/apt/weewx.list | tee /etc/apt/sources.list.d/weewx.list
COPY ./docker/install_weewx.py .
RUN python3 install_weewx.py
RUN rm install_weewx.py
COPY ./docker/weewx.conf /etc/weewx/


# App
WORKDIR /root/
COPY ./transfer-system/ .
RUN pipenv install --system --skip-lock
RUN pip install -r requirements-server.txt


# Config
COPY ./docker/weewx.empty.sdb /var/lib/weewx/weewx.sdb


# Clean up
RUN pip uninstall -y pexpect


ENTRYPOINT ["make", "run.server"]
