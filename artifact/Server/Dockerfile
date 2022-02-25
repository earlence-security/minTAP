#Download base image ubuntu 20.04
FROM ubuntu:20.04

RUN apt-get update

ENV NODE_VERSION=10.19
   RUN apt-get update && \
       apt-get install wget curl ca-certificates rsync -y
   RUN wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.33.2/install.sh | bash
   ENV NVM_DIR=/root/.nvm
   RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
   RUN . "$NVM_DIR/nvm.sh" &&  nvm use v${NODE_VERSION}
   RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
   RUN cp /root/.nvm/versions/node/v${NODE_VERSION}/bin/node /usr/bin/
   RUN cp /root/.nvm/versions/node/v${NODE_VERSION}/bin/npm /usr/bin/
   RUN /root/.nvm/versions/node/v${NODE_VERSION}/bin/npm install  leasot@latest -g