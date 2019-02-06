# Programming Assignment2--
# Fan Feng
# Email: ffeng2@crimson.ua.edu
# date: 2019-2-5

# -----------------------------------------------------------------------
# twitter-stream-format:
#  - ultra-real-time stream of twitter's public timeline.
#    does some fancy output formatting.
# -----------------------------------------------------------------------

import re

# -----------------------------------------------------------------------
# load our API credentials
# -----------------------------------------------------------------------
import sys
import json
import time
import config
sys.path.append(".")

# To make the ANSI colors used in termcolor work with the windows terminal,
#  you'll need to also import/init colorama;
import colorama
colorama.init()

# set the search_term to "#" to get all tweets with hashtags
search_term = "#"

# -----------------------------------------------------------------------
# import a load of external features, for text display and date handling
# you will need the termcolor module:
#
# pip install termcolor
# -----------------------------------------------------------------------
from twitter import *

from time import strftime
from textwrap import fill
from termcolor import colored
from email.utils import parsedate

#-----------------------------------------------------------------------
# create twitter streaming API object
#-----------------------------------------------------------------------
auth = OAuth(config.access_key,
             config.access_secret,
             config.consumer_key,
             config.consumer_secret)

stream = TwitterStream(auth = auth, secure = True)

pattern = re.compile("%s" % search_term, re.IGNORECASE)


#-----------------------------------------------------------------------
# iterate over tweets matching this filter text
#-----------------------------------------------------------------------
tweet_iter = stream.statuses.filter(track=search_term)

result = []
for i,tweet in enumerate(tweet_iter):
    if not i: # start time
        t1 = parsedate(tweet["created_at"])
    result.append(tweet)
    # turn the date string into a date object that python can handle
    timestamp = parsedate(tweet["created_at"])

    # now format this nicely into HH:MM:SS format
    timetext = strftime("%H:%M:%S", timestamp)

    # colour our tweet's time, user and text
    time_colored = colored(timetext, color = "yellow", attrs = [ "bold" ])
    user_colored = colored(tweet["user"]["screen_name"], "green")
    text_colored = tweet["text"]

    # replace each instance of our search terms with a highlighted version
    text_colored = pattern.sub(colored(search_term.upper(), "red"), text_colored)

    # add some indenting to each line and wrap the text nicely
    indent = " " * 11
    text_colored = fill(text_colored, 80, initial_indent = indent, subsequent_indent = indent)

    # now output our tweet
    print("(%s) @%s" % (time_colored, user_colored))
    print("%s" % (text_colored))

    if time.mktime(timestamp) - time.mktime(t1) >= 600: # After 10 minutes
        t2 = timestamp # end time
        with open('result.json','w') as fp:
            json.dump(result,fp)
        break

print(t1,timestamp)
#  Count the number of each hashtag
hashtags_dict = {}
for tweet in result:
    hashtags = tweet['entities'].get('hashtags')
    for hashtag in hashtags:
        if hashtag['text'] in hashtags_dict.keys():
            hashtags_dict[hashtag['text']] += 1
        else:
            hashtags_dict[hashtag['text']] = 1
# sort all the hashtags and get the top 10
to10_hashtags = sorted(hashtags_dict, key = hashtags_dict.get,reverse = True)[:10]
print(sorted(hashtags_dict, key = hashtags_dict.get,reverse = True)[:10])
with open("result.txt",mode = 'w', encoding ='utf-8') as fp:
    fp.write("%s \t %s \n"%(time.strftime("%Y-%m-%d %H:%M:%S", t1),time.strftime("%Y-%m-%d %H:%M:%S", t2)))
    for key in to10_hashtags:
        fp.write("%s \t %d \n"%(key,hashtags_dict[key]))

