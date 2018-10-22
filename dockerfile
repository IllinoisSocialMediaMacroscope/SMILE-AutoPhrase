FROM ubuntu:18.04

# git clone autophrase algorithm
RUN apt-get -y update
RUN apt-get -y install git
RUN cd / && git clone https://github.com/IllinoisSocialMediaMacroscope/SMILE-AutoPhrase.git AutoPhrase

# install dependency libraries
RUN apt-get -y install g++
RUN apt-get -y install openjdk-8-jdk
RUN apt-get -y install curl
RUN apt-get -y install python3-pip
RUN pip3 install numpy pandas boto3

# switch work directory to be AutoPhrase
RUN cd /AutoPhrase && /bin/bash -c "source compile.sh"
WORKDIR /AutoPhrase