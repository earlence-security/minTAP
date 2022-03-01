#!/bin/bash

cd isolated_server
npm install 
node server &

cd ..

export FLASK_APP=service
mkdir instance
flask init-db
flask run &
