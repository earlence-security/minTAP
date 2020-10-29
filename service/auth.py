import time
import json
import secrets

import sqlite3
import requests
from flask import Blueprint, request, redirect

ifttt_redirect_uri = ''
oauth_code = ''
access_token = ''

code_challenge = ''
public_key = ''

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route("authorize", methods=['GET'])
def authorize():
    # handle misformatted requests
    client_id = request.args['client_id']
    state = request.args['state']

    global ifttt_redirect_uri
    ifttt_redirect_uri = request.args['redirect_uri']

    reddit_auth_url = f'https://ssl.reddit.com/api/v1/authorize?response_type=code&' \
                      f'scope=edit,history,identity,modconfig,modflair,modlog,modposts,mysubreddits,privatemessages,read,save,submit,subscribe,vote&' \
                      f'client_id={client_id}&' \
                      f'redirect_uri=http://35.222.210.67:5000/auth/callback&' \
                      f'duration=permanent&' \
                      f'state={state}'

    print('auth')
    # print(reddit_auth_url)

    if 'code_challenge' in request.args:
        print('code_challenge received')
        global code_challenge
        code_challenge = request.args['code_challenge']

    if 'public_key' in request.args:
        print('public key received')
        global public_key
        public_key = request.args['public_key']

    return redirect(reddit_auth_url)


@bp.route("callback", methods=['GET', 'POST'])
def callback():
    state = request.args['state']

    global oauth_code
    oauth_code = request.args['code']

    print('callback')
    print(request.args)

    return redirect(f'{ifttt_redirect_uri}?state={state}&code={oauth_code}')


@bp.route("token", methods=['GET', 'POST'])
def token():
    print('token')
    print(request.form)

    code = request.form['code']
    # client_id = request.form['client_id']
    # client_secret = request.form['client_secret']

    if 'code_verifier' not in request.form:
        return {"token_type": "Bearer", "access_token": secrets.token_hex(40)}

    reddit_token_url = 'https://www.reddit.com/api/v1/access_token'

    response = requests.post(
        url=reddit_token_url,
        headers={
            'User-agent': 'mock ifttt',
            "Authorization": "Basic a3lWXzIwWTdIc092UlE6cVdnZ3BOcG5ESDJxYzcyUHk1MEpXYkYwTDJn",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        },
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://35.222.210.67:5000/auth/callback",
        }
    )

    print('response from reddit')
    data = json.loads(response.content)
    print(data)

    global access_token
    access_token = data['access_token']

    return {"token_type": "Bearer", "access_token": access_token}
