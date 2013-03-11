#!/bin/bash
source /home/adam/.virtualenvs/rescraper/bin/activate

SCRIPT=$(readlink -f $0)
SCRIPTPATH=$(dirname $SCRIPT)

${SCRIPTPATH}/manage.py collect_data

echo "Last ran on: " + $(date) >> ${SCRIPTPATH}/scheduled.txt
