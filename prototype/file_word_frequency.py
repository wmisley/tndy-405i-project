import nltk
import operator
from nltk.probability import FreqDist

fileurl = "/Users/will4769/Downloads/readme.txt"
file_y = open(fileurl)
p = file_y.read()
words = nltk.tokenize.word_tokenize(p)
fdist = FreqDist(words)

for key in fdist:
    print key, ": ", fdist[key]

sorted_x = sorted(fdist.items(), key=operator.itemgetter(1), reverse=True)

for key in sorted_x:
    print("'" + str(key[0]) + "'," + str(key[1]))

