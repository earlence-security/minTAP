import time
import json
import os
import atexit
from urllib.parse import unquote

import sqlite3
import requests
from flask import Blueprint, request, current_app
from apscheduler.schedulers.background import BackgroundScheduler

from service.db import get_db


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


bp = Blueprint('trigger', __name__, url_prefix='/ifttt/v1/triggers')

trigger_identity = ''




@bp.route("mintap_toy_trigger", methods=['GET', 'POST'])
def new_test_data():
    # handle misformatted requests
    if request.headers['Authorization'] != 'Bearer ' + current_app.config['ACCESS_TOKEN']:
        return {'errors': [{'message': 'invalid token'}]}, 401

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

    if 'author' not in request_body['triggerFields'] or 'code_signature' not in request_body['triggerFields'] or \
            'filter_code' not in request_body['triggerFields']:
        return {"errors": [
            {
                "message": "missing trigger fields"
            }
        ]}, 400

    # print(unquote(request_body['triggerFields']['filter_code']))

    # get trigger fields from request
    limit = 50 if 'limit' not in request_body else request_body['limit']

    author = request_body['triggerFields']['author']

    db = get_db()
    data = []

    # get trigger data from database
    cur = db.cursor()
    sql = 'SELECT * FROM test_data WHERE author=?'
    cur.execute(sql, (author,))

    rows = cur.fetchall()

    count = 0
    for row in rows:

        if count >= limit:
            break

        event = {'author': row[1],
                 'title': row[2],
                 'content': row[3],
                 'post_url': row[4],
                 'meta': {
                     'id': row[0],
                     'timestamp': row[5]
                 }}

        print(f"{bcolors.OKCYAN}Original: {event}{bcolors.ENDC}")

        # response = requests.post('http://localhost:3000/filter',
        #                          headers={"Content-Type": "application/json; charset=utf-8"},
        #                          data=json.dumps({'data': {
        #                              'Author': row[1],
        #                              'Title': row[2],
        #                              'Content': row[3],
        #                              'PostUrl': row[4],
        #                          }, 'filter': unquote(request_body['triggerFields']['filter_code'].replace('%C2%A0', '%20'))}))
        #
        # accessed = json.loads(response.content.decode())['result']
        #
        #
        # if accessed == 'skip':
        #     print(f"{bcolors.OKGREEN}SKIP{bcolors.ENDC}")
        #     continue
        #
        # if 'Author' not in accessed:
        #     event['author'] = ''
        # if 'Title' not in accessed:
        #     event['title'] = ''
        # if 'Content' not in accessed:
        #     event['content'] = ''
        # if 'PostUrl' not in accessed:
        #     event['post_url'] = ''
        #
        # print(f"{bcolors.OKGREEN}Sent: {event}{bcolors.ENDC}")

        count += 1

        data.append(event)

    data.sort(key=lambda e: e['meta']['timestamp'], reverse=True)

    return {'data': data}


@bp.route("feed_test_data", methods=['GET', 'POST'])
def feed_test_data():
    db = get_db()

    request_body = json.loads(request.data)

    sql = '''INSERT OR IGNORE INTO test_data(id,author,title,content,post_url,timestamp)
                 VALUES(?,?,?,?,?,?) '''


    db.cursor().execute(sql, (request_body['id'],
                              request_body['author'],
                              request_body['title'],
                              request_body['content'],
                              request_body['post_url'],
                              int(time.time())))

    db.commit()

    requests.post('https://realtime.ifttt.com/v1/notifications', data={'user_id': 'heisenberg'})

    return 'success'
