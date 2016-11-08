import ystockquote
from pprint import pprint

#pprint(ystockquote.get_historical_prices('BIS', '2016-09-16', '2016-09-18'))


pprint(ystockquote.get_historical_prices('AAPL', '2016-10-26', '2016-10-26'))

#t= ystockquote.get_historical_prices('AAA', '2013-01-03', '2013-01-08')
#rint(t.get('2013-01-03').get('Adj Close'))

