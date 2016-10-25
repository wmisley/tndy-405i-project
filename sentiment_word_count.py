from sentiment_dictionary import DictionaryReader
from company_list import CompanyFileReader
from tweet_list import TweetFileReader
from tweet_sentiment_company_decorator import TweetDecorator

sentiment_dict_file = "data/SentiWordNet_3.0.0_20130122.txt"
company_list_file = "data/companylist.csv"
twitter_file = "/Users/will4769/Downloads/Tweets/jessefelder_tweets.log"

reader = DictionaryReader(sentiment_dict_file)
words = reader.parse()

for key, val in words.items():
    print(val.term + ":" + val.pos_score + ":" + val.neg_score)

company_reader = CompanyFileReader(company_list_file)
comp_dict = company_reader.parse()

for key, val in comp_dict.items():
    print(val.symbol + ":" + val.name)

twitter_reader = TweetFileReader(twitter_file)
tweets = twitter_reader.parse("AswathDamodaran")

tweet_dec = TweetDecorator(words, comp_dict)
cst_list = tweet_dec.add_sentiment_words(tweets)
tweet_dec.output(cst_list)



