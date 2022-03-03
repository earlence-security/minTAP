#!/bin/bash

mkdir -p /mintap_log

cd isolated_server
npm install 
node server > /mintap_log/node_log 2>&1 &

cd ..

export FLASK_APP=service
mkdir instance
flask init-db
flask run > /mintap_log/flask_log 2>&1 &
