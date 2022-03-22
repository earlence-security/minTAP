#Download base image ubuntu 20.04
FROM ubuntu:20.04

RUN apt-get update

ENV DEBIAN_FRONTEND=noninteractive

# Install node stuff
RUN apt-get install -y nodejs npm
# install python stuff
RUN apt-get install -y python3.6 python3-distutils python3-pip python3-apt

RUN echo "Python Packages" 
RUN pip3 install flask requests cryptography

WORKDIR minTAP
ADD isolated_server isolated_server
ADD service service

USER root
COPY setup.sh .
RUN chmod +x setup.sh 

WORKDIR /minTAP/isolated_server
RUN npm install

WORKDIR /minTAP
ENTRYPOINT /minTAP/setup.sh

