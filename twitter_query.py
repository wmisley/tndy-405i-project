#Go to https://apps.twitter.com and create an app

import tweepy

consumer_key = "n2WebZuPpCWG9xguQ9Nx6sJLW"
consumer_secret = "WTfshJzVzrSaWuT4hjEtlV6KivAQa79unN9eCCGIrtduQtQ8vr"
access_token = "70616645-l81XYFgtS7E9a2WsrlC5OHE8OqM2ywC3aV28MPMMN"
access_token_secret = "67r1dgZvJwhse1z8hl026pSsZESwkuzVZfRekBdvvqTct"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#    print tweet.text

public_tweets = api.user_timeline("Oracle")

for tweet in public_tweets:
    print tweet.text