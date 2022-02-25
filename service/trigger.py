import time
import json
import os
import atexit
from urllib.parse import unquote

import praw
import sqlite3
import requests
from flask import Blueprint, request, current_app
from apscheduler.schedulers.background import BackgroundScheduler

from service.db import get_db

reddit = praw.Reddit(client_id='kyV_20Y7HsOvRQ',
                     client_secret='qWggpNpnDH2qc72Py50JWbF0L2g',
                     redirect_uri="http://localhost:8080",
                     user_agent="testscript")

bp = Blueprint('trigger', __name__, url_prefix='/ifttt/v1/triggers')

trigger_identity = ''

apsched = BackgroundScheduler()
apsched.start()
atexit.register(lambda: apsched.shutdown())


def fetch_top_post(db_path, subreddit):
    db = sqlite3.connect(
        db_path,
        detect_types=sqlite3.PARSE_DECLTYPES
    )

    sql = '''INSERT OR IGNORE INTO top_post(id,subreddit,title,content,post_url,timestamp)
                 VALUES(?,?,?,?,?,?) '''

    for submission in reddit.subreddit(subreddit).top(time_filter='day', limit=10):
        content = submission.selftext if submission.is_self else submission.url

        db.cursor().execute(sql, (submission.id,
                                  submission.subreddit_name_prefixed,
                                  submission.title,
                                  content,
                                  submission.url,
                                  int(submission.created)))

    db.commit()

    return


@bp.route("new_top_post", methods=['GET', 'POST'])
def new_top_post():
    # handle misformatted requests
    # if request.headers['IFTTT-Channel-Key'] != current_app.config['CHANNEL_KEY']:
    #     return {"errors": [
    #         {
    #             "message": "invalid ifttt channel key"
    #         }
    #     ]}, 401

    request_body = json.loads(request.data)

    if 'triggerFields' not in request_body:
        return {"errors": [
            {
                "message": "missing trigger fields"
            }
        ]}, 400

    if 'subreddit' not in request_body['triggerFields'] or 'code_signature' not in request_body['triggerFields'] or \
            'filter_code' not in request_body['triggerFields']:
        return {"errors": [
            {
                "message": "missing trigger fields"
            }
        ]}, 400

    # get trigger fields from request
    limit = 50 if 'limit' not in request_body else request_body['limit']

    subreddit = request_body['triggerFields']['subreddit']

    db = get_db()
    data = []

    # check if background job for subreddit is running
    if apsched.get_job(subreddit) is None:
        sql = '''INSERT OR IGNORE INTO top_post(id,subreddit,title,content,post_url,timestamp)
                         VALUES(?,?,?,?,?,?) '''

        for submission in reddit.subreddit(subreddit).top(time_filter='day', limit=10):
            content = submission.selftext if submission.is_self else submission.url

            db.cursor().execute(sql, (submission.id,
                                      submission.subreddit_name_prefixed,
                                      submission.title,
                                      content,
                                      submission.url,
                                      int(submission.created)))

        db.commit()

        apsched.add_job(fetch_top_post, trigger='interval', args=(current_app.config['DATABASE'], subreddit),
                        minutes=1, id=subreddit)

    # get trigger data from database
    cur = db.cursor()
    sql = 'SELECT * FROM top_post WHERE subreddit=?'
    cur.execute(sql, ('r/' + subreddit,))

    rows = cur.fetchall()

    count = 0
    for row in rows:

        if count >= limit:
            break

        event = {'subreddit': row[1],
                 'title': row[2],
                 'content': row[3],
                 'post_url': row[4],
                 'meta': {
                     'id': row[0],
                     'timestamp': row[5]
                 }}
        print(row)

        count += 1

        data.append(event)

    data.sort(key=lambda e: e['meta']['timestamp'], reverse=True)

    return {'data': data}


@bp.route("new_test_data", methods=['GET', 'POST'])
def new_test_data():
    # handle misformatted requests
    # if request.headers['IFTTT-Channel-Key'] != current_app.config['CHANNEL_KEY']:
    #     return {"errors": [
    #         {
    #             "message": "invalid ifttt channel key"
    #         }
    #     ]}, 401

    request_body = json.loads(request.data)

    if 'trigger_identity' in request_body:
        global trigger_identity
        trigger_identity = request_body['trigger_identity']

    if 'triggerFields' not in request_body:
        return {"errors": [
            {
                "message": "missing trigger fields"
            }
        ]}, 400

    if 'subreddit' not in request_body['triggerFields'] or 'code_signature' not in request_body['triggerFields'] or \
            'filter_code' not in request_body['triggerFields']:
        return {"errors": [
            {
                "message": "missing trigger fields"
            }
        ]}, 400

    # print(unquote(request_body['triggerFields']['filter_code']))

    # get trigger fields from request
    limit = 50 if 'limit' not in request_body else request_body['limit']

    subreddit = request_body['triggerFields']['subreddit']

    db = get_db()
    data = []

    # get trigger data from database
    cur = db.cursor()
    sql = 'SELECT * FROM test_data'
    cur.execute(sql)

    rows = cur.fetchall()

    count = 0
    for row in rows:

        if count >= limit:
            break

        event = {'subreddit': row[1],
                 'title': row[2],
                 'content': row[3],
                 'post_url': row[4],
                 'meta': {
                     'id': row[0],
                     'timestamp': row[5]
                 }}

        class bcolors:
            HEADER = '\033[95m'
            OKBLUE = '\033[94m'
            OKCYAN = '\033[96m'
            OKGREEN = '\033[92m'
            WARNING = '\033[93m'
            FAIL = '\033[91m'
            ENDC = '\033[0m'
            BOLD = '\033[1m'
            UNDERLINE = '\033[4m'

        print(f"{bcolors.OKCYAN}Original: {event}{bcolors.ENDC}")

        response = requests.post('http://localhost:3000/filter',
                                 headers={"Content-Type": "application/json; charset=utf-8"},
                                 data=json.dumps({'data': {
                                     'Subreddit': row[1],
                                     'Title': row[2],
                                     'Content': row[3],
                                     'PostUrl': row[4],
                                 }, 'filter': unquote(request_body['triggerFields']['filter_code'].replace('%C2%A0', '%20'))}))

        accessed = json.loads(response.content.decode())['result']


        if accessed == 'skip':
            print(f"{bcolors.OKGREEN}SKIP{bcolors.ENDC}")
            continue

        if 'Subreddit' not in accessed:
            event['subreddit'] = ''
        if 'Title' not in accessed:
            event['title'] = ''
        if 'Content' not in accessed:
            event['content'] = ''
        if 'PostUrl' not in accessed:
            event['post_url'] = ''

        print(f"{bcolors.OKGREEN}Sent: {event}{bcolors.ENDC}")

        count += 1

        data.append(event)

    data.sort(key=lambda e: e['meta']['timestamp'], reverse=True)

    return {'data': data}


@bp.route("feed_test_data", methods=['GET', 'POST'])
def feed_test_data():
    db = get_db()

    request_body = json.loads(request.data)

    sql = '''INSERT OR IGNORE INTO test_data(id,subreddit,title,content,post_url,timestamp)
                 VALUES(?,?,?,?,?,?) '''

    requests.post('https://realtime.ifttt.com/v1/notifications', data={'user_id': 'heisenberg'})

    db.cursor().execute(sql, (request_body['id'],
                              request_body['subreddit'],
                              request_body['title'],
                              request_body['content'],
                              request_body['post_url'],
                              int(time.time())))

    db.commit()

    return ''
