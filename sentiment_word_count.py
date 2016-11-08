from sentiment_dictionary import DictionaryReader
from company_list import CompanyFileReader
from tweet_list import TweetFileReader
from tweet_sentiment_company_decorator import TweetDecorator, CompanySentimentTweetWriter
import os

sentiment_dict_file = "data/SentiWordNet_3.0.0_20130122.txt"
company_list_file = "data/companylist.csv"
twitter_file = "/Users/will4769/Downloads/Tweets/jessefelder_tweets.log"


def create_decorated_files(tweet_folder, words, comp_dict):
    cst_mast_list = []

    try:
        for file_name in os.listdir(tweet_folder):
            file_path = os.path.join(tweet_folder, file_name)

            if os.path.isfile(file_path):
                print(file_name)
                if file_name.split("_")[1] == "tweets.log":
                    print("Processing " + file_path)
                    tweeter = file_name.split("_")[0]

                    twitter_reader = TweetFileReader(file_path)
                    tweets = twitter_reader.parse(tweeter)

                    tweet_dec = TweetDecorator(words, comp_dict)
                    cst_list = tweet_dec.add_sentiment_words(tweeter, tweets)
                    cst_mast_list.extend(cst_list)

    except:
        print("Error reading data")

    print("Writing out data")
    cst_writer = CompanySentimentTweetWriter(cst_mast_list)
    full = "/tmp/full.log"
    comp = "/tmp/comp.log"
    cst_writer.write_to_file(full, comp)



print("Reading sentiment dictionary")
reader = DictionaryReader(sentiment_dict_file)
words = reader.parse()

print("Reading company file")
company_reader = CompanyFileReader(company_list_file)
comp_dict = company_reader.parse()

full = "/tmp/full.log"
comp = "/tmp/comp.log"

if os.path.exists(full):
    os.unlink(full)

if os.path.exists(comp):
    os.unlink(comp)

print("Creating decorated twitter log")
create_decorated_files("/Users/will4769/Downloads/Tweets", words, comp_dict)





