import nltk
import ystockquote
from tweet_list import TweetRecord
from company_list import CompanyStockRecord
from nltk.probability import FreqDist


class CompanySentimentTweet:
    sent_rec_dict = {}
    comp_rec_list = []
    tweet_rec = TweetRecord()

    def __init__(self):
        self.sent_rec_dict = {}
        self.comp_rec_list = []
        self.tweet_rec = None

    def __init__(self, tweet, dictionary_record_dict=None, company_record_list=None):
        self.sent_rec_dict = dictionary_record_dict
        self.comp_rec_list = company_record_list
        self.tweet_rec = tweet


class TweetDecorator:
    sent_dict = {}
    comp_dict = {}
    comp_ignor_dict = {'BV':'BV'}

    def __init__(self, sentiment_dictionary, company_dictionary):
        self.sent_dict = sentiment_dictionary
        self.comp_dict = company_dictionary

    def get_company_stock_rec(self, company_rec, tweet):
        # format 2016-10-08 12:28:36
        date = tweet.created_at[0:10]
        symbol = company_rec.symbol
        result = ystockquote.get_historical_prices(symbol, date, date)
        print(symbol)
        print(date)
        print(result)
        print(result.get(date))
        return result.get(date)

    def add_sentiment_words(self, tweets):
        cst_list = []
        tweet_count = 0

        for tweet in tweets:
            sent_list = {}
            comp_list = []
            tweet_count += 1
            print(str(tweet_count) + ":" + tweet.tweet_text)
            tweet_text = tweet.decode_text()
            words = nltk.tokenize.word_tokenize(tweet_text)
            freq_dist = FreqDist(words)

            # for each word in the tweet
            for word, count in freq_dist.items():
                # get the words with sentiment from the tweet
                sent_rec = self.sent_dict.get(word)
                if not (sent_rec is None):
                    sent_list[sent_rec.term] = sent_rec

                # get companies from the tweet and add stock price
                if self.comp_ignor_dict.get(word) is None:
                    company = self.comp_dict.get(word)
                    if not (company is None):
                        if not any(comp.company.symbol == word for comp in comp_list):
                            stock_result = self.get_company_stock_rec(company, tweet)
                            c = CompanyStockRecord(company, stock_result)
                            comp_list.append(c)

            cst = CompanySentimentTweet(tweet, sent_list, comp_list)
            cst_list.append(cst)

        return cst_list

    def output(self, cst_list):
        for cst in cst_list:
            if (len(cst.sent_rec_dict) > 0) and (len(cst.comp_rec_list) > 0):
                print("------------")
                print(cst.tweet_rec.tweet_text)

                print("words:")
                if len(cst.sent_rec_dict) > 0:
                    for key, sent_rec in cst.sent_rec_dict.items():
                        print(sent_rec.term + ":" + str(sent_rec.pos_score) + ":" + str(sent_rec.neg_score))

                print("company:")
                for comp_rec in cst.comp_rec_list:
                    print(comp_rec.company.name + ":" + str(comp_rec.close))
