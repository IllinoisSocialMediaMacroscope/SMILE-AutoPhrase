FROM ubuntu:18.04

RUN mkdir -p /scripts
WORKDIR /scripts

# copy paste scripts
COPY . ./

# install dependency libraries
RUN apt-get update
RUN apt-get -y install g++
RUN apt-get -y install openjdk-8-jdk
RUN apt-get -y install curl
RUN apt-get -y install python3-pip
RUN pip3 install numpy pandas boto3 plotly

# switch work directory to be AutoPhrase
RUN cd /scripts && /bin/bash -c "source compile.sh"
WORKDIR /scripts