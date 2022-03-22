
# minTAP Server
This folder contains the implementation of a minTAP-compatible service and the instructions on how to set up a Docker container to host the service. The minTAP-compatible service mimics existing services on IFTTT and provide a test trigger. It consists of two pieces: (1) A Python server that integrates minTAP’s protocol with current IFTTT APIs, and (2) A runtime environment that can securely execute transformed filter code for dynamic minimization.


## Software dependencies
Everything is provided within the containers. So no need to install anything beyond that. 

##  Installation

1. Install docker

```
sudo apt  install docker.io
```

2. Follow the instructions below for setting up the docker container (make sure inbound traffic is allowed on port `5000`).

```
cd mintap/Server
sudo docker build -t mintap .
sudo docker run -it -p 127.0.0.1:5000:5000 mintap
```

## Usage

The service is registered as `minTAP example service` in IFTTT and provides a test IFTTT trigger `Toy Trigger`. 

1. You may manually fire the trigger with the curl command:

```
curl -X "POST" "[DOCKER URL]:5000/ifttt/v1/triggers/feed_test_data" \
     -H 'Content-Type: application/json; charset=utf-8' \
     -d $'{
  "author": "Alice",
  "title": "Example Title",
  "content": "Example Content",
  "post_url": "www.example.com"
}'
```
where `DOCKER URL` is the public address of the host machine running the docker container, and the payload's values can be freely modified.

2. After the rule is run, you can check each rule's activity log to confirm if the unneeded data are sanitized (i.e. appears as none).

![alt text](https://raw.githubusercontent.com/EarlMadSec/minTAP/master/screenshot_0.jpg)

![alt text](https://raw.githubusercontent.com/EarlMadSec/minTAP/master/screenshot_1.jpg)