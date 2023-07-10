from textblob import TextBlob
import textblob
import tweepy 
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# Connection to the api
api_key = 'f9QDFkLm0hRjJtlqSZMTTEvxZ'
api_key_secret = 'CiS03yMWCwX7Xhubw3AF8wU79F5bDpdU0VtHsC8K24oWBEt7NT'
access_token = '1223293246681559042-jSkfiFCdGtpHTcFMOS7zqvaOWVYmBm'
access_token_secret = 'ITPw91RpeO6ONMiLuKfE8cOeQnHZOvpDSx2oRoOGHn1QL'

#bearer_token = 'AAAAAAAAAAAAAAAAAAAAANNjCQEAAAAA0tQMCT0VtM7NNbjKb5pY%2BUqnzyU%3D5XXmWifVd9R7LJL08OHXaDzdOZttCxETPAycpbsIMCqmxzwSmU'
            # o de cima ê novo tbm

authenticator = tweepy.OAuthHandler(api_key, api_key_secret) 
authenticator.set_access_token(access_token, access_token_secret) 

api = tweepy.API(authenticator, wait_on_rate_limit=True)

#api.update_status("Hello Tweepy")  # new code]

#client = tweepy.Client(bearer_token=) # editado



crypto_currency = 'Ethereum'

search = f'#{crypto_currency} -filter:retweets'

tweet_cursor = tweepy.Cursor(api.search_tweets, q=search, lang='en', tweet_mode='extended').items(100) # api.search_tweets

tweets = [tweet.full_text for tweet in tweet_cursor]

tweets_df = pd.DataFrame(tweets, columns=['Tweets'])

for _, row in tweets_df.iterrows():
    row['Tweets'] = re.sub('http\S+', '', row['Tweets'])
    row['Tweets'] = re.sub('#\S+', '', row['Tweets'])
    row['Tweets'] = re.sub('@\S+', '', row['Tweets'])
    row['Tweets'] = re.sub('\\n', '', row['Tweets'])

tweets_df['Polarity'] = tweets_df['Tweets'].map(lambda tweet: textblob.TextBlob(tweet).sentiment.polarity)
tweets_df['Result'] = tweets_df['Polarity'].map(lambda pol: '+' if pol > 0 else '-')


positive = tweets_df[tweets_df.Result == '+'].count()['Tweets']
negative = tweets_df[tweets_df.Result == '-'].count()['Tweets']

print(positive, negative)

plt.bar([0], [positive], label=['Positive'], color=['green'])
plt.bar([1], [ negative], label=['Negative'], color=['red'])
plt.legend()
plt.show() 


