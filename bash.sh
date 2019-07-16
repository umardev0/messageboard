#!/bin/bash
while true; do
	if redis-cli ping |grep PONG; then
		break
	else
		echo "Redis not running. Make sure redis is running at localhost:6379"
		sleep 5
	fi
done

java -jar CreateMessage/createmessage.jar &
java_pid=$!
python3 -m venv ListMessages/venv
source ListMessages/venv/bin/activate
pip install -U pip
sleep 5
pip install -r ListMessages/requirements.txt
sleep 10
python ListMessages/app.py

trap "kill $java_pid" EXIT