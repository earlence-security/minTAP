# Abstract
This artifacts consists of a set of IFTTT rules with corresponding filter code. Our experiments in Section 7 can be reproduced using the provided Docker machines and companion scripts.

# Description
The artifact folder consists of a docker machine. This machine hosts the shim service that we used to mimic IFTTT cloud. The shim on service’s compatibility layer that runs on the server docker consists of two pieces: (1) A Python library that will upgrade thetrigger service’s APIs so that they can engage in minTAP’sprotocol, and (2) A runtime environment that can securely execute transformed filter code for dynamic minimization.

<!-- 1- **The first docker machine** runs the client browser extension. We implement the client as a Chrome extension that monitors the user’s interactions withthe IFTTT webpage by analyzing the endpoints being visited. For example, it will launch the authorization phase if the user visits URLs like ifttt.com/[service]/redirect_to_connect.    -->

## How to access
You can use the following link to clone the artifacts. 
## Software dependencies
Everything is provided within the containers. So no need to install anything beyond that. The evaluator needs to have: `chrome browser` and `docker` installed on their machine. 

## Data sets
Among the crawled IFTTT rules, in this artifact we are using 554 IFTTT rules that contain filter code. The filter code files are in JavaScript.
#  Installation
Please follow the following instructions for installing and running the docker machine.

```
cd Server
docker build -t mintap .
docker run -it mintap
```

# Experiment workflow
The experiment comprises 3 components:  

1- Testing the functionality of minTAP. 

2- Reporducing privacy benefit (Section 7.2)

3- Reporoducing latency and throughput experiments (Section 7.3)



# Evaluation and expected results
Following is a description of the instructions for running various components of minTAP and the expected results after running each component.
## Testing the functionality of minTAP:

## Reporducing privacy benefit

## Reporoducing latency and throughput experiments

