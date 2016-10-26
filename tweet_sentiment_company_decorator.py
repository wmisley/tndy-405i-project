import nltk
import ystockquote
import time
import datetime
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

    def calc_next_business_day(self, date_time_str):
        # format 2016-10-08 12:28:36
        date_str = date_time_str.split(" ")[0]
        year, month, day = (int(x) for x in date_str.split('-'))
        date = datetime.date(year, month, day)

        if not date.isoweekday():
            date +=datetime.timedelta(days=1)
            if not date.isoweekday():
                date +=datetime.timedelta(days=1)

        return date.strftime('%Y-%m-%d')

    def get_company_stock_rec(self, company_rec, tweet):
        # format 2016-10-08 12:28:36
        date = tweet.created_at[0:10]
        symbol = company_rec.symbol
        next_business_day = self.calc_next_business_day(date)
        print("symbol:" + symbol)
        print("date:" + date)
        print("next business day: " + next_business_day)
        result = None

        try:
            result = ystockquote.get_historical_prices(symbol, next_business_day, next_business_day)
        except:
            print("Error calling ystockquote.get_historic_prices()")
            time.sleep(10)
            return None

        else:
            print("result:" + str(result))
            print("result date:" + str(result.get(date)))
            return result.get(date)

    def add_sentiment_words(self, tweets):
        cst_list = []
        tweet_count = 0

        for tweet in tweets:
            sent_dict = {}
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
                    if not (sent_rec.term in sent_dict):
                        sent_dict[sent_rec.term] = sent_rec
                    else:
                        sent_dict[sent_rec.term].increment_count()

                # get companies from the tweet and add stock price
                if self.comp_ignor_dict.get(word) is None:
                    company = self.comp_dict.get(word)
                    if not (company is None):
                        if not any(comp.company.symbol == word for comp in comp_list):
                            stock_result = self.get_company_stock_rec(company, tweet)
                            if not (stock_result is None):
                                c = CompanyStockRecord(company, stock_result)
                                comp_list.append(c)

            cst = CompanySentimentTweet(tweet, sent_dict, comp_list)
            cst_list.append(cst)

        return cst_list


class CompanySentimentTweetWriter:
    cst_list = []

    def __init__(self, comp_sent_list):
        self.cst_list = comp_sent_list

    def get_csv_header(self, high_freq_words_list):
        header = "#tweeter,"
        header += "company.symbol,"
        header += "company.name,"
        header += "company.last_sale,"
        header += "company.market_cap,"
        header += "company.ipo_year,"
        header += "company.sector,"
        header += "company.industry,"
        header += "company.summary_quote,"
        header += "stock.adj_close,"
        header += "stock.close,"
        header += "stock.high,"
        header += "stock.low,"
        header += "stock.open,"
        header += "stock.volume,"

        header += "tweet.id_str,"
        header += "tweet.text,"
        header += "tweet.retweet_count,"
        header += "tweet.favorite_count,"
        header += "tweet.created_at,"
        header += "tweet.place,"
        header += "tweet.source,"
        header += "tweet.coordinates,"

        for freq_word in high_freq_words_list:
            header += freq_word + "_count,"

        return header[:-1]

    def get_company_csv_rec(self, comp_stock_rec):
        csv_record = str(comp_stock_rec.company.symbol) + ","
        csv_record += "\"" + comp_stock_rec.company.name + "\","
        csv_record += str("{0:.2f}".format(float(comp_stock_rec.company.last_sale))) + ","
        csv_record += str(comp_stock_rec.company.market_cap) + ","
        csv_record += str(comp_stock_rec.company.ipo_year) + ","
        csv_record += str(comp_stock_rec.company.sector) + ","
        csv_record += "\"" + str(comp_stock_rec.company.industry) + "\","
        csv_record += str(comp_stock_rec.company.summary_quote) + ","

        csv_record += str("{0:.2f}".format(float(comp_stock_rec.adj_close))) + ","
        csv_record += str("{0:.2f}".format(float(comp_stock_rec.close))) + ","
        csv_record += str("{0:.2f}".format(float(comp_stock_rec.high))) + ","
        csv_record += str("{0:.2f}".format(float(comp_stock_rec.low))) + ","
        csv_record += str("{0:.2f}".format(float(comp_stock_rec.open))) + ","
        csv_record += str("{0:.2f}".format(float(comp_stock_rec.volume))) + ","

        return csv_record

    def get_tweet_csv_rec(self, tweet):
        csv_record = tweet.tweet_id + ","
        csv_record += "\"" + tweet.tweet_text.replace("\n", "").replace("\"", "\"\"") + "\","
        csv_record += str(tweet.retweet_count) + ","
        csv_record += str(tweet.favorite_count) + ","
        csv_record += str(tweet.created_at) + ","
        csv_record += "\"" + str(tweet.place).replace("\n", "").replace("\"", "\"\"") + "\","
        csv_record += "\"" + str(tweet.source).replace("\n", "").replace("\"", "\"\"") + "\","
        csv_record += "\"" + str(tweet.coordinates) + "\","

        return csv_record

    def get_word_csv_rec(self, high_freq_words_list, sent_rec_dict):
        csv_record = ""
        for freq_word in high_freq_words_list:
            if freq_word in sent_rec_dict:
                csv_record += str(sent_rec_dict[freq_word].count) + ","
            else:
                csv_record += "0,"
        return csv_record[:-1]

    def write_to_file(self, tweeter, full_file_path, comp_file_path):
        high_freq_words_list = self.get_freq_weighted_sentiment_words(50)

        full_csv_file = open(full_file_path, 'a')
        comp_csv_file = open(comp_file_path, 'a')

        header = self.get_csv_header(high_freq_words_list)
        print(header)
        full_csv_file.write(header + "\n")
        comp_csv_file.write(header + "\n")

        for cst in self.cst_list:
            for comp_stock_rec in cst.comp_rec_list:
                csv_record = tweeter + ","
                csv_record += self.get_company_csv_rec(comp_stock_rec)
                csv_record += self.get_tweet_csv_rec(cst.tweet_rec)
                csv_record += self.get_word_csv_rec(high_freq_words_list, cst.sent_rec_dict)

                print(csv_record)
                full_csv_file.write(csv_record + "\n")
                comp_csv_file.write(csv_record + "\n")

        full_csv_file.close()
        comp_csv_file.close()

    def get_freq_sentiment_words(self, count):
        high_freq_words = {}

        # build a dict of all words that are common across tweets
        for cst in self.cst_list:
            if len(cst.comp_rec_list) > 0:
                for word, sent_rec in cst.sent_rec_dict.items():
                    if not (word in high_freq_words):
                        high_freq_words[word] = sent_rec
                    else:
                        high_freq_words[word].increment_total_count()

        return sorted(high_freq_words, key=lambda w: high_freq_words[w].total_count, reverse=True)[: count]

    def get_freq_weighted_sentiment_words(self, count):
        high_freq_words = {}

        # build a dict of all words that are common across tweets
        for cst in self.cst_list:
            if len(cst.comp_rec_list) > 0:
                for word, sent_rec in cst.sent_rec_dict.items():
                    if not (word in high_freq_words):
                        high_freq_words[word] = sent_rec
                    else:
                        high_freq_words[word].increment_total_count()

        return sorted(high_freq_words, key=lambda w: (high_freq_words[w].total_count * abs(float(high_freq_words[w].neg_score) + float(high_freq_words[w].pos_score))), reverse=True)[: count]

    def output(self):
        for cst in self.cst_list:
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
