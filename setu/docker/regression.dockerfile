FROM python:3.8.2-buster
USER root
COPY . /usr/src/app

# Install OpenJDK-11
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean;

RUN useradd -ms /bin/bash ksaha
RUN echo "ksaha:password" | chpasswd

# Change to kiran user
USER ksaha

COPY --chown=ksaha ./setu/ /setu

RUN mkdir -p /home/ksaha/.pip
COPY ./setu/pip.conf /home/ksaha/.pip
RUN pip install --user --upgrade pip
RUN LC_CTYPE="en_US.UTF-8" pip install --user -r /setu/requirements.txt
RUN pip install --user --upgrade setuptools


WORKDIR /home/ksaha
# Install allure binary
RUN curl "https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.17.0/allure-commandline-2.17.0.tgz" -o "/home/ksaha/allure-commandline-2.17.0.tgz"
RUN tar -xvf /home/ksaha/allure-commandline-2.17.0.tgz -C /home/ksaha/

