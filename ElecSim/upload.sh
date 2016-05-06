#!/bin/sh
SITE=http://rpifq.no-ip.org:8000/upload/
JSON=MY_CONFIGURE.json
FAMILY=1
FILE=MY_FILE.csv
PROGRAM=main.py
NOW=$(date --date="next minute" +"%Y-%m-%dT%H:%M")
EARLIER=$(date +"%Y-%m-%dT%H:%M")

python3 $PROGRAM --mode=generate --config_file=$JSON --household=$FAMILY --from=$EARLIER --to=$NOW --output=$FILE

curl -F "Uplfile=@$FILE" -F "household=$FAMILY"  $SITE
