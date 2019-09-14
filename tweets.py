#!/usr/bin/env python
# encoding: utf-8
#Author - Prateek Mehta


import tweepy #https://github.com/tweepy/tweepy
import json
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

#Twitter API credentials
consumer_key = "cDQiT2swOorc6vix3iyilxuOA"
consumer_secret = "5xNfHUZfvKu8mZ9Xl9XUKDB0iRL0gDhrQ7lauyTy2xUbQr2GAW"
access_key = "1556542249-u5a8d6jVfhNC0S2QgFEWsbmTqh7hOibY5Br7qRd"
access_secret = "ra0TXYvo2xn53tiJHvve8q4tPy2pPzP8YhTQmYd5uCqHz"


def get_all_tweets(screen_name):
    
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    client = language.LanguageServiceClient()
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=10)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=10,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
       
            

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        if(len(alltweets) > 15):
            break
        print("...%s tweets downloaded so far" % (len(alltweets)) )
       
    #write tweet objects to JSON
    file = open('tweet.json', 'w') 
    print("Writing tweet objects to JSON please wait...")
    for status in alltweets:
        json.dump(status._json,file,sort_keys = True,indent = 4)
    
    #close the file
    print("Done")
    file.close()



    for t in alltweets:

        text=t.text
        print("%s"%t.text)
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)
        print("\nAnalysis:\n")
        # Detects the sentiment of the text
        sentiment = client.analyze_sentiment(document=document).document_sentiment
        keywords = client.analyze_entities(document=document).entities
        print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
        print("keywords:\n")
        for e in keywords:
            print(e.name, e.salience)
        print("===============================================================")










if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets("@elonmusk")