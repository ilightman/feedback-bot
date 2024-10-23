#!/usr/bin/env bash
BASEDIR=$(dirname "$0")
echo "Executing App in '$BASEDIR'"
PORT=$1
source $BASEDIR/feedbackbot/venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 80 --ssl-certfile=$BASEDIR/YOURPUBLIC.pem --ssl-keyfile=$BASEDIR/YOURPRIVATE.key
#python $BASEDIR/main.py $PORT
