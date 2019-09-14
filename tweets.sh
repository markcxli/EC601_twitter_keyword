#!/bin/bash
export GOOGLE_APPLICATION_CREDENTIALS=tweetAnalyzer-965deefe97e3.json
source env/bin/activate
# if have not installed google natual language or tweepy yet
sudo pip install google-natural-language
sudo pip install tweepy

python tweets.py 