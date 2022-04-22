#!/bin/bash

# move to the activities directory
cd /Users/kylekent/Library/CloudStorage/Dropbox/cycling_analytics/strava_expore_04-15-22;
# unzip all the .fit.gz files
gzip -d *.fit.gz;
# run the py file to convert all the fit files to csv
python3 fit2csv.py;
# remove the unnecessary csv files of laps and starts
rm *_laps.csv *_starts.csv;
