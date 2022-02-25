## Environment Setup

We tested this artifact under Ubuntu 20.04 LTS and Python 3.8.

Install the required Python libraries: 

```
$ pip3 install flask requests praw apscheduler click celery
```

## Start the server



```
cd minTAP/
export FLASK_APP=service

mkdir instance
flask init-db

flask run
```
