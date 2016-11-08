import pandas as pd

import scipy as sp
df= pd.read_csv('/tmp/tweet_stock.log', usecols=['stock.close',
                                                                                      'tweet.retweet_count',
                                                                                      'tweet.favorite_count'])




stock_retweet_cor = sp.stats.pearsonr([df.stock_close],[df.retweet_count])
stock_fav_cor = sp.stats.pearsonr([df.stock_close],[df.favorite_count])