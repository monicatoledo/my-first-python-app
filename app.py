import os
import pandas as pd
import tweepy
import time
import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# Uncomment the following to test the script locally:
#from config import consumer_key, consumer_secret, access_token, access_token_secret

analyzer = SentimentIntensityAnalyzer()

# Get config variable from environment variables // Comment if testing locally
consumer_key = os.environ.get("consumer_key")
consumer_secret = os.environ.get("consumer_secret")
access_token = os.environ.get("access_token")
access_token_secret = os.environ.get("access_token_secret")

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


def update_twitter():

    mentions = api.search(q="@PlotBot Analyze:")
    #print(mentions)
    words = []
    # Lists to hold sentiments
    compound_list = []
    positive_list = []
    negative_list = []
    neutral_list = []

    # Variable for tweets ago
    counter=0
    tweets_ago=[]
    command = mentions["statuses"][0]["text"]
    words = command.split("Analyze:")
    target_user = words[1].strip()
        
    for x in range(8):
        try:
            public_tweets=api.user_timeline(target_user,page=x)
        # Loop through tweets
            for tweet in public_tweets:

                result=analyzer.polarity_scores(tweet['text'])
                tweets_ago.append(counter)
                compound_list.append(result['compound'])
                positive_list.append(result['pos'])
                negative_list.append(result['neg'])
                neutral_list.append(result['neu'])
                counter+=1
        except:
            print('error in reading tweets')
            
    # Convert dictionary to DataFrame
    data={'Tweets Ago':tweets_ago, 'Compound': compound_list, 'Positive': positive_list,'Neutral': neutral_list, 'Negative':negative_list}
    data_df=pd.DataFrame(data)

    # Create plot
    plt.plot(data_df['Tweets Ago'], data_df['Compound'], marker="o", linewidth=0.5,
         alpha=0.8)

    # Incorporate the other graph properties
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M")
    plt.title(f"Sentiment Analysis of Tweets ({now}) for {target_user}")
    plt.ylabel("Tweet Polarity")
    plt.xlabel("Tweets Ago")
    
    plt.savefig("plot1.png")
    api.update_with_media(
            "plot1.png", "Tweet Polarity " + target_user
        )

    # Grab Self Tweets
    tweets = api.user_timeline()

    # Confirm the target account has never been tweeted before
    repeat = False

    for tweet in tweets:
        if target_user in tweet["text"]:
            repeat = True
            print("Sorry. Repeat detected!")

        else:
            continue


# Have the Twitter bot update every five minutes for two days
days = 0
while days < 2:
print("Updating Twitter")

    # Update the twitter
    update_twitter()

    # Wait 5 minutes
    time.sleep(300)

    # Update day counter
    days += 1