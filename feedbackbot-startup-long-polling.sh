#!/usr/bin/env bash
echo "starting feedback bot"
cd /web/bots/
. ./feedbackbot/.venv/bin/activate
echo "venv activated"
python3 ./feedbackbot/main-long-polling.py &
