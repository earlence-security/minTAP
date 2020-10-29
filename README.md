# Mock Reddit Service for IFTTT

Available endpoints:
- `/ifttt/v1/status`
- `/ifttt/v1/test/setup`
- `/ifttt/v1/triggers/new_top_post`

Python packages required:
- Flask
- APScheduler

How to run:
1. Set up `IFTTT_CHANNEL_KEY`, `REDDIT_CLIENT_ID`, and `REDDIT_CLIENT_SECRET` environment variables
2. Run 
```
$ export FLASK_APP=service
$ flask init-db
$ flask run
```
