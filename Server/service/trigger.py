import time
import json
import os
import uuid
import base64
from urllib.parse import unquote
from pprint import pprint
from pathlib import Path

import sqlite3
import requests
from flask import Blueprint, request, current_app
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

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


LATENCY_LOG = Path('./latency.log')


@bp.route("mintap_toy_trigger", methods=['GET', 'POST'])
def toy_trigger():
    # handle misformatted requests
    if request.headers['Authorization'] != 'Bearer ' + current_app.config['ACCESS_TOKEN']:
        return {'errors': [{'message': 'invalid token'}]}, 401

    request_body = json.loads(request.data)

    pprint(request_body)

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


    minimizer = unquote(request_body['triggerFields']['filter_code'])
    signature = base64.b64decode(request_body['triggerFields']['code_signature'])
    print(minimizer.encode())
    print(signature)
    try:
        pk = load_pem_public_key(Path(current_app.config['PUBLIC_KEY_FILE']).read_bytes())
        pk.verify(signature, minimizer.encode(), padding.PKCS1v15(), hashes.SHA256())
    except:
        print('signature error')



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

        response = requests.post('http://localhost:3000/filter',
                                 headers={"Content-Type": "application/json; charset=utf-8"},
                                 data=json.dumps({'data': {
                                     'Author': row[1],
                                     'Title': row[2],
                                     'Content': row[3],
                                     'PostUrl': row[4],
                                 }, 'filter': unquote(request_body['triggerFields']['filter_code'].replace('%C2%A0', '%20'))}))

        accessed = json.loads(response.content.decode())['result']


        if accessed == 'skip':
            print(f"{bcolors.OKGREEN}SKIP{bcolors.ENDC}")
            continue

        if 'Author' not in accessed:
            event['author'] = ''
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

    sql = '''INSERT OR IGNORE INTO test_data(id,author,title,content,post_url,timestamp)
                 VALUES(?,?,?,?,?,?) '''


    db.cursor().execute(sql, (uuid.uuid1().int>>96,
                              request_body['author'],
                              request_body['title'],
                              request_body['content'],
                              request_body['post_url'],
                              int(time.time())))

    db.commit()

    response = requests.post('https://realtime.ifttt.com/v1/notifications', headers={'IFTTT-Service-Key': current_app.config['CHANNEL_KEY']},
                             json={'data': [{'user_id': 'heisenberg'}]})

    print(response.content)

    return 'success'




@bp.route("bench", methods=['GET'])
def bench():
    # handle misformatted requests
    test_input = {'author': 'Alice',
                  'code_signature': '36iVB8KCUg09IGlYcl8Ky8AVjV7XZyRGFvqj21CJ+O0Od2dbthqNAddT3CFkVpKp41hSgboorlyvE+Knu7qqN7WzKqph/UM36I+n+t5o3XBDFu/oFMoq6Rc95VdM6o0erTE/8y2Mb+2kLSDQGl7gVs19Fq1VY/7EfpqnjX+FI6zExad+uzS26ZnfcyhRCPW8BKC9azL3yIgsOeUgLLxBcvZkbKv/YyYgTVyODmS/2feo5x8Ab1X7vwJMRQpYmfx4dLIvXPmOdKO9Z0pmm3YPHTPJSR1p3byBjdKS9gzSJDJDtW4gIFQrAtjjppWYWpJyMvo/FPlWZy2e7TX4rtml6A==',
                  'filter_code': "%0Afunction%20filter(data)%20%7B%0Avar%20data2%20=%20data.copy()%0Aconst%20Trigger%20=%20new%20mintapToyTrigger(data2);%0Aconst%20MintapService%20=%20%7BmintapToyTrigger:%20Trigger%7D;%0Aconst%20Action%20=%20new%20DummyAction();%0A%0Alet%C2%A0x%C2%A0=%C2%A0MintapService.mintapToyTrigger.Title%0A%C2%A0%0Aif%C2%A0(x%C2%A0===%C2%A0'Demo%C2%A0Skip%C2%A0Title')%C2%A0%7B%0A%C2%A0%C2%A0return%20null;%0A%7D%0A%C2%A0%0AAction.action(MintapService.mintapToyTrigger.Content)%0AAction.action(MintapService.mintapToyTrigger.Title)%0A%20%20%20%20%0Areturn%20MintapService.mintapToyTrigger.accessedFields();%0A%0A%7D%20%20%20%0A"}

    latencies = []
    for _ in range(20):
        latency = 0
        t0 = time.time()

        minimizer = unquote(test_input['filter_code'])
        signature = base64.b64decode(test_input['code_signature'])
        try:
            pk = load_pem_public_key(Path(current_app.config['PUBLIC_KEY_FILE']).read_bytes())
            pk.verify(signature, minimizer.encode(), padding.PKCS1v15(), hashes.SHA256())
        except:
            pass

        t1 = time.time()
        latency += t1 - t0


        # get trigger fields from request
        limit = 1

        author = 'Alice'

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

            t0 = time.time()
            response = requests.post('http://localhost:3000/filter',
                                     headers={"Content-Type": "application/json; charset=utf-8"},
                                     data=json.dumps({'data': {
                                         'Author': row[1],
                                         'Title': row[2],
                                         'Content': row[3],
                                         'PostUrl': row[4],
                                     }, 'filter': unquote(test_input['filter_code'].replace('%C2%A0', '%20'))}))

            accessed = json.loads(response.content.decode())['result']


            if accessed == 'skip':
                continue

            if 'Author' not in accessed:
                event['author'] = ''
            if 'Title' not in accessed:
                event['title'] = ''
            if 'Content' not in accessed:
                event['content'] = ''
            if 'PostUrl' not in accessed:
                event['post_url'] = ''

            t1 = time.time()
            latency += t1 - t0

            count += 1

            data.append(event)

        data.sort(key=lambda e: e['meta']['timestamp'], reverse=True)

        print(latency)
        latencies.append(latency)

    return {'extra_latency': sum(latencies) / len(latencies)}
