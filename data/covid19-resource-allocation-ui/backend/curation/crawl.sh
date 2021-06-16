#!/bin/bash
# very basic script to run get_esri_data.py every 30 minutes

interval=1800
echo "Start crawling every $interval seceonds." > crawling.log
while [[ ! -f /home/dx7fu/stop_crawling.txt ]] ; do
    now=$(date +%s) # timestamp in seconds
    echo "Crawling done at "`date` >> crawling.log
    python get_esri_data.py           
    sleep $((interval - now % interval))
done
