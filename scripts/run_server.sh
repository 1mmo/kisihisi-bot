#!/bin/bash

VENV=./venv
DEPLOY_FLAG=/opt/kisihisi/deploy_state.flag

touch $DEPLOY_FLAG

if [ ! -d $VENV ]; then
    `which python3` -m venv $VENV
    $VENV/bin/pip install -U pip
fi
`which python3` -m venv $VENV
$VENV/bin/pip install -U pip

$VENV/bin/pip install -r requirements.txt

$VENV/bin/python3 src/manage.py migrate
$VENV/bin/python3 src/manage.py collectstatic --no-input

$VENV/bin/python3 src/manage.py runserver 0.0.0.0:8000

rm -f $DEPLOY_FLAG

echo "Run Django"
