#!/bin/sh
SITE=http://127.0.0.1:8000/upload/
JSON=MY_CONFIGURE.json
FAMILY=2
FILE=MY_FILE.csv
PROGRAM=main.py
NOW=$(date --date="next minute" +"%Y-%m-%dT%H:%M")
EARLIER=$(date +"%Y-%m-%dT%H:%M")

python3 $PROGRAM --mode=generate --config_file=$JSON --household=$FAMILY --from=$EARLIER --to=$NOW --output=$FILE

curl -F "Uplfile=@$FILE" -F "household=$FAMILY"  $SITE
