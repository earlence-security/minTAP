#!/bin/bash

mkdir -p /mintap_log

cd isolated_server
node server > /mintap_log/node_log 2>&1 &

cd ..

export FLASK_APP=service
mkdir instance
flask init-db

flask run --host=0.0.0.0 > /mintap_log/flask_log 2>&1 
