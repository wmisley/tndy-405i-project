import tweepy
import nltk
import operator
import sys
import os
from nltk.probability import FreqDist
import time
import datetime

reload(sys)
sys.setdefaultencoding('utf8')


tweet_log_folder = "/Users/will4769/Downloads/Tweets"
twitter_user = "MarketPlunger"
consumer_key = ""
consumer_secret = ""
access_token = "70616645-"
access_token_secret = ""
folder_separator = "/"
max_query_times = 180


def log_tweet_word_frequency(raw_text_file_path, word_freq_file_path):
    print("Calculating word frequency")
    text_file = open(raw_text_file_path)
    wf_file = open(word_freq_file_path, "a")
    text = text_file.read()

    udata = text.decode("utf-8")
    asciidata = udata.encode("ascii","ignore")

    words = nltk.tokenize.word_tokenize(asciidata)
    fdist = FreqDist(words)

    sorted_words = sorted(fdist.items(), key=operator.itemgetter(1), reverse=True)

    for key in sorted_words:
        wf_file.write(str(key[0]) + "," + str(key[1]) + "\n")
        #print(str(key[0]) + "," + str(key[1]))

    text_file.close()
    wf_file.close()


def log_tweets(tweets, csv_file_path, raw_text_file_path):
    csv_file = open(csv_file_path, 'a')
    text_file = open(raw_text_file_path, 'a')

    for tweet in tweets:
        csv_record = tweet.id_str + ","
        csv_record += "\"" + tweet.text.replace("\n", "").replace("\"", "\"\"") + "\","
        csv_record += str(tweet.retweet_count) + ","
        csv_record += str(tweet.favorite_count) + ","
        csv_record += str(tweet.created_at) + ","
        csv_record += "\"" + str(tweet.place).replace("\n", "").replace("\"", "\"\"") + "\","
        csv_record += "\"" + str(tweet.source).replace("\n", "").replace("\"", "\"\"") + "\","
        csv_record += "\"" + str(tweet.coordinates) + "\""
        print(csv_record)
        csv_file.write(csv_record.encode("utf-8") + "\n")
        text_file.write(tweet.text.encode("utf-8"))

    csv_file.close()
    text_file.close()


def query_tweets(user_id, tweet_csv_log, tweet_raw_tex_log):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    print("Getting tweets from user: " + user_id)
    statuses = api.user_timeline(id=user_id,count=200)
    query_count = 1

    log_tweets(statuses, tweet_csv_log, tweet_raw_tex_log)

    while len(statuses) > 0:
        oldest_id = statuses[-1].id - 1
        statuses = api.user_timeline(id=user_id,count=200,max_id=oldest_id)
        query_count += 1

        log_tweets(statuses, tweet_csv_log, tweet_raw_tex_log)

        # TODO: Find a way to work around Twitter API limit of 180 queries every 15 min
        if query_count == max_query_times:
            print("Max tweek queries reached, sleeping 15 min.")
            print(datetime.datetime.now())
            query_count = 1
            time.sleep(60*15)


tweet_csv_log = tweet_log_folder + folder_separator + twitter_user + "_tweets.log"
tweet_raw_tex_log = tweet_log_folder + folder_separator + twitter_user + "_raw_text.log"
word_freq_file_path = tweet_log_folder + folder_separator + twitter_user + "_word_freq.log"

if os.path.exists(tweet_csv_log):
    os.unlink(tweet_csv_log)

if os.path.exists(tweet_raw_tex_log):
    os.unlink(tweet_raw_tex_log)

if os.path.exists(word_freq_file_path):
    os.unlink(word_freq_file_path)

query_tweets(twitter_user, tweet_csv_log, tweet_raw_tex_log)
log_tweet_word_frequency(tweet_raw_tex_log, word_freq_file_path)
