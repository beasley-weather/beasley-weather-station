FROM ubuntu:xenial


ARG PASS="pass"
ENV USER="badger"


# RUN useradd -m $USER
# RUN echo $USER:$PASS | chpasswd


# Install packages
RUN apt-get update && \
    apt-get -y install \
      curl \
      locales \
      python \
      python-pip \
      python3 \
      python3-pip \
      tzdata \
      wget
RUN pip3 install pipenv


# Timezone and Locale
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV TZ=America/Toronto
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
RUN locale-gen


ENTRYPOINT bash
