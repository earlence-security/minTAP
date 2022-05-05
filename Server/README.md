
# minTAP Server
This folder contains the implementation of a minTAP-compatible service and the instructions on how to set up a Docker container to host the service. The minTAP-compatible service mimics existing services on IFTTT and provide a test trigger. It consists of two pieces: (1) A Python server that integrates minTAP’s protocol with current IFTTT APIs, and (2) A runtime environment that can securely execute transformed filter code for dynamic minimization.


## Software dependencies
Everything is provided within the containers. So no need to install anything beyond that. 

##  Installation

1. Install docker

```
sudo apt  install docker.io
```

2. Follow the instructions below for setting up the docker container (make sure inbound traffic is allowed on port 5000).

```
cd mintap/Server
sudo docker build -t mintap .
sudo docker run -d -p 5000:5000 mintap
```
Now the minTAP-compatible service should be live on the host machine's port 5000. 

## IFTTT Registration

The service should be registered as `minTAP example service` in IFTTT and provide a test IFTTT trigger `Toy Trigger`. 

1. Create a developer account at https://ifttt.com/developers.

1. Create a new service in https://ifttt.com/services/new. 
In the remaining steps, we assume the service is named `mintap_service`.

1. Create a new trigger for the service, set the `Endpoint` field to `mintap_toy_trigger` and add the following trigger fields and ingredients.

![alt text](https://raw.githubusercontent.com/EarlMadSec/minTAP/master/screenshots/screenshot_6.jpg)

![alt text](https://raw.githubusercontent.com/EarlMadSec/minTAP/master/screenshots/screenshot_7.jpg)


1. In the `API` tab of the service (e.g., https://platform.ifttt.com/services/mintap_service/api), fill the `IFTTT API URL` field with the URL path to the minTAP-compatible service (i.e., port 5000 on the server host machine). 

1. Select `Authentication` in the `API` tab (e.g., https://platform.ifttt.com/services/mintap_service/api/authentication), fill the `Authorization URL` field with `[IFTTT API URL]/mintap/auth/authorize` and the `Token URL` field with `[IFTTT API URL]/mintap/auth/token`.


## Usage


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

![alt text](https://raw.githubusercontent.com/EarlMadSec/minTAP/master/screenshots/screenshot_0.jpg)

![alt text](https://raw.githubusercontent.com/EarlMadSec/minTAP/master/screenshots/screenshot_1.jpg)