# Abstract
This artifacts consists of a set of IFTTT rules with corresponding filter code. Our experiments in Section 7 can be reproduced using the provided Docker machines. For running the docker machines, you need XXX. 

# Description
The artifact folder consists of two docker machines. 

1- **The first docker machine** runs the client browser extension. We implement the client as a Chrome extension that monitors the user’s interactions withthe IFTTT webpage by analyzing the endpoints being visited. For example, it will launch the authorization phase if the user visits URLs like ifttt.com/[service]/redirect_to_connect.   

2- **The second docker machine** hosts the shim service that we used to mimic IFTTT cloud. The shim on service’s compatibility layer that runs on the server docker consists of two pieces: (1) A Python library that will upgrade thetrigger service’s APIs so that they can engage in minTAP’sprotocol, and (2) A runtime environment that can securely execute transformed filter code for dynamic minimization.



## How to access
You can use the following link to clone the artifacts. 
## Software dependencies
Everything is provided within the containers. So no need to install anything beyond that.
## Data sets
Among the crawled IFTTT rules, in this artifact we are using 554 IFTTT rules that contain filter code. The filter code files are in JavaScript.
#  Installation
Please follow the following instructions for installing and running the docker machines.

```
```

# Experiment workflow
After running the two docker machines, a connection will be established between the two machines over the port <>.  

# Evaluation and expected results
## Replicating the results Section 7.3:
