#!/bin/sh
FILE=MY_FILE.csv
JSON=MY_CONFIGURE.json
PROGRAM=main.py
SITE=http://91.176.207.129:5901/upload/
FAMILY=1
NOW=$(date +"%Y-%m-%dT%H:%M")
EARLIER=$(date --date="1 minutes ago" +"%Y-%m-%dT%H:%M")

python3 $PROGRAM --mode=generate --config_file=$JSON --household=$FAMILY --from=$EARLIER --to=$NOW --output=$FILE

curl -F "Uplfile=@$FILE" -F "household=$FAMILY"  $SITE
