# tndy-405i-project
This project is a set of Python scripts developed for the TNDY 405I Data Analytical Tools, Technologies, and
Applications Across The Disciplines class at Claremont Graduate University (CGU)

# Features
This project is a set of scripts that supports pulling data from Twitter feeds and online stock market APIs.

# Research Question

What predictors can be developed from tweets of “influential economist” to predict stock price trends?

The predictors that will be explored are variables such as:

*	Words or phases that have more or less impact
    Which words have greater or lesser impact on stock price when found in tweets (Examples: “fear”, “rise”, “fall”, …)? Is there consistency across different “influential economist’s” tweets and different company’s’ stock prices?

*	Term frequency impact
    Does the count of certain words have a greater or lesser impact on stock prices? Is this consistent across different “influential economist’s” tweets and different company’s stock prices?

*	Tweeter centrality
    Does the “influential economist’s” centrality have a greater or lesser impact on stock prices? Is this consistent across different “influential economist’s” tweets and different company’s stock prices?


# Prerequisites

* Python 2.7.10
* Tweepy


If you do not have the Tweepy package, do the following

```
git clone https://github.com/tweepy/tweepy.git
cd tweepy
python setup.py install
```

# Resources

MarkitOnDemand REST API:
http://dev.markitondemand.com/MODApis/

Twitter REST API:
https://dev.twitter.com/rest/public

Tweepy Python Package:
https://github.com/tweepy/tweepy
