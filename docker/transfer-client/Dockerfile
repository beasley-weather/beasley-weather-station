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


USER badger
ENTRYPOINT ["make", "run.client"]
