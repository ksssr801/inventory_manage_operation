#!/bin/zsh

INSTDIR="$( cd "$( dirname "${(%):-%N}" )" && pwd )"
SOURCEDIR="$(dirname "$INSTDIR")"

cd /opt
source InvManageEnv/bin/activate
cd $INSTDIR

start() {
    python manage.py runserver 0.0.0.0:9000
}

start
