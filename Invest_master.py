import tweepy
import re
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import matplotlib.pyplot as plt
import os

# need modification!!! ++++++++++++++++++++++++++++++++++++++++++++++
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/robertmorrislike/PycharmProjects/EC601_MiniProject/another.json"


class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def Analyze(self):
        # authenticating
        consumerKey = "8FAsDfpjf5ulYEUwLIU7uMJwR"
        consumerSecret = "S53RD6tK9p6y5023VAGA3MGrixCjpmAynRFkq2Sncwp9XT1LLG"
        accessToken = "1171844680603951104-IkD9C423Cy8lE0nlEn3P7HKMnEhHNg"
        accessTokenSecret = "QfXNAtJTiwkBVLLj9feA3QXLoBXwr3Hl53dduolGL9Wol"
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        # input for term to be searched and how many tweets to search
        keyword = input("Enter Keyword/Tag to search about: ")
        numOfTweets = int(input("Enter how many tweets to search: "))

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=keyword, lang = "en").items(numOfTweets)

        # pre-set sentiment values
        Negative = 0
        Neutral = 0
        Positive = 0


        # iterating through tweets fetched
        for tweet in self.tweets:
            # clean up each tweet acquired
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            # using Google API to get sentiment score
            sentiment_score = self.get_sentiment_score(tweet.text)
            if sentiment_score <= -0.25:
                Negative += 1
            elif sentiment_score <= 0.25:
                Neutral += 1
            else:
                Positive += 1

        negative = format(100 * float(Negative) / float(numOfTweets), '.2f')
        neutral = format(100 * float(Neutral) / float(numOfTweets), '.2f')
        positive = format(100 * float(Positive) / float(numOfTweets), '.2f')

        self.plotPieChart(positive,negative,neutral, keyword, numOfTweets)

        print()
        print("Detailed Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(negative) + "% people thought it was negative")
        print(str(neutral) + "% people thought it was neutral")


    def get_sentiment_score(self,tweet):
        client = language.LanguageServiceClient()
        document = types \
            .Document(content=tweet,
                      type=enums.Document.Type.PLAIN_TEXT)
        sentiment_score = client \
            .analyze_sentiment(document=document) \
            .document_sentiment \
            .score
        return sentiment_score


    def cleanTweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    def plotPieChart(self, positive, negative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]','Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]']
        sizes = [positive, neutral, negative]
        colors = ['yellowgreen', 'gold', 'darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('The Twitter Reflection on ' + searchTerm + ' after analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()


if __name__== "__main__":
    test = SentimentAnalysis()
    test.Analyze()
