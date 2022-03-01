import time
import json
import secrets

import sqlite3
import requests
from flask import Blueprint, request, redirect, current_app

ifttt_redirect_uri = ''
oauth_code = secrets.token_hex(40)

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

    if 'code_challenge' in request.args:
        print('code_challenge received')
        global code_challenge
        code_challenge = request.args['code_challenge']

    if 'public_key' in request.args:
        print('public key received')
        global public_key
        public_key = request.args['public_key']

    return redirect(f'{ifttt_redirect_uri}?state={state}&code={oauth_code}')


# @bp.route("callback", methods=['GET', 'POST'])
# def callback():
#     state = request.args['state']
#
#     global oauth_code
#     oauth_code = request.args['code']
#
#     print('callback')
#     print(request.args)
#
#     return redirect(f'{ifttt_redirect_uri}?state={state}&code={oauth_code}')


@bp.route("token", methods=['GET', 'POST'])
def token():
    print('token')
    print(request.form)

    code = request.form['code']
    client_id = request.form['client_id']
    client_secret = request.form['client_secret']

    if oauth_code != code or current_app.config['CLIENT_ID'] != client_id \
            or current_app.config['CLIENT_SECRET'] != client_secret:
        return '', 400

    if 'code_verifier' not in request.form:
        return {"token_type": "Bearer", "access_token": current_app.config['ACCESS_TOKEN']}

    code_verifier = request.form['code_verifier']

    if code_verifier != code_challenge:
        return '', 400


    return {"token_type": "Bearer", "access_token": secrets.token_hex(40)}
