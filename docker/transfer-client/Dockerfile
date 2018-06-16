FROM beasley_weather_base:latest


ENV PASS="pass"
ENV USER="badger"


RUN useradd -m $USER
RUN echo $USER:$PASS | chpasswd


# App
USER badger
WORKDIR /home/$USER
COPY ./transfer-system/ .
USER root
RUN pipenv install --system --skip-lock
RUN pip install -r requirements-client.txt


# Cleanup
# UNCOMMENT BEFORE PROD
# RUN apt-get -y purge curl git wget && apt-get -y autoclean && apt-get -y autoremove


USER badger
ENTRYPOINT ["make", "run.client"]
