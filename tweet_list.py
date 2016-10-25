import csv

class TweetRecord:
    tweeter = ""
    tweet_id = ""
    tweet_text = ""
    retweet_count = 0
    favorite_count = 0
    created_at = ""
    place = ""
    source = ""
    coordinates = ""

    def __init__(self):
        self.tweeter = ""
        self.tweet_id = ""
        self.tweet_text = ""
        self.retweet_count = 0
        self.favorite_count = 0
        self.created_at = ""
        self.place = ""
        self.source = ""
        self.coordinates = ""
        self.sentiment_words = []
        self.companies_mentioned = []

    def decode_text(self):
        utf_data = self.tweet_text.decode("utf-8")
        ascii_data = utf_data.encode("ascii", "ignore")
        return ascii_data


class TweetFileReader:
    __file_path = ""

    def __init__(self, file_path):
        self.__file_path = file_path

    def parse(self, tweeter):
        tweets = []
        with open(self.__file_path, 'r') as f:
            next(f)
            reader = csv.reader(filter(lambda row: row[0] != '#', f), delimiter=',')

            line = 0

            for tweet_id, tweet_text, retweet_count, favorite_count, created_at, place, source, coordinates in reader:
                tweet = TweetRecord()
                tweet.tweeter = tweeter
                tweet.tweet_id = tweet_id
                tweet.tweet_text = tweet_text
                tweet.retweet_count = retweet_count
                tweet.favorite_count = favorite_count
                tweet.created_at = created_at
                tweet.place = place
                tweet.source = source
                tweet.coordinates = coordinates

                tweets.append(tweet)

                line += 1
                print(line)

        return tweets

