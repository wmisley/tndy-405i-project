import tweepy
import time
import sys

#Search
#Search is rate limited at 180 queries per 15 minute window.
#https://dev.twitter.com/rest/public/timelines


consumer_key = 'n2WebZuPpCWG9xguQ9Nx6sJLW'
consumer_secret = 'WTfshJzVzrSaWuT4hjEtlV6KivAQa79unN9eCCGIrtduQtQ8vr'
access_token = '70616645-l81XYFgtS7E9a2WsrlC5OHE8OqM2ywC3aV28MPMMN'
access_token_secret = '67r1dgZvJwhse1z8hl026pSsZESwkuzVZfRekBdvvqTct'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

filename = 'data38.csv'

saveFile = open(filename, 'a')

user_id = ['WarrenBuffett', 'aswathdamodaran']
#user_id = ['WarrenBuffett']

listofword = ['hope', 'happy', 'fear', 'worry','nervous','anxious','upset', 'positive', 'negative']
companylist = ['AAPL','Apple Inc']

teststring = 'fear and FEAR and worry and upset and what I can do, NERVOUS'



def checkCompany(companylist, str_check_company):

    for i in range (len(companylist)):
        if companylist[i].lower() in str_check_company.lower():
            return '1'
    return '0'
    saveFile.write('\t')

def checkWord(listofword, str_check_word):
    counter = 0
    frequency = []
    total_number_of_word = len(str_check_word.split())
    frequency.append(total_number_of_word)
    for i in range (len(listofword)):
        y = listofword[i]
        if y in str_check_word.lower():
            counter = str_check_word.lower().count(y)
            frequency.append( counter )
        else:
            frequency.append( 0 )
        #print (listofword[i], counter)
        #print ('\n')
    return frequency
#print (frequency)


def getTweet(user_id):
    #initialize a list to hold all the tweepy Tweets
    alltweets = []

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(id=user_id ,count=200)

    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print ("getting tweets before %s" % (oldest))

        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(id=user_id,count=200,max_id=oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print ("...%s tweets downloaded so far" % (len(alltweets)))

        for tweet in alltweets:

    #transform the tweepy tweets into a 2D array
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]


    for i in range(len(outtweets)):
        saveFile.write(user_id)
        saveFile.write('\t')
        str_check_company = str(outtweets[i][2])
        y = checkCompany(companylist, str_check_company)
        saveFile.write(y)
        saveFile.write('\t')
        #Frequency_of_word = []


        Frequency_of_word = checkWord(listofword, str(outtweets[i][2]))

        for fre in range (len (Frequency_of_word)) :
            saveFile.write('\t')
            saveFile.write(str(Frequency_of_word[fre]))
            saveFile.write('\t')


        for j in range (len(outtweets[i])):
            print(outtweets[i][j], end = '\t')
            saveFile.write(str(outtweets[i][j]))
            saveFile.write('\t')
        #str_check_company = str(outtweets[i][2])
        print('\n')
        saveFile.write('[end of tweets here]')
        saveFile.write('\t')
        saveFile.write('\n')


for i in range(len(user_id)):
    getTweet(user_id[i])



saveFile.close()

################test function###############
#checkWord(listofword, teststring)