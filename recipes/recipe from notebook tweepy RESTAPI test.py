# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
%pylab inline

import dataiku
from dataiku import pandasutils as pdu
import pandas as pd

import tweepy

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
atoken = "1211674579879391233-VwxwWZO0nnio8wwBVzncqhjfCTmz8S"
asecret = "SUNhejwVlBrsx1B8I7yqXkn9NzjOKR6kzejkAHmJHdOTP"
ckey = "nSLLEuipKq6iJetBCLj33mv1J"
csecret = "s9XGj7t3XMvsmX2EHWeUHex2VvthapZFmmpFAj40VsQV2SvnVg"

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Replace the API_KEY and API_SECRET with your application's key and secret.
auth = tweepy.AppAuthHandler(ckey, csecret)

api = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
import sys
import jsonpickle
import os

searchQuery = 'Air France'  # this is what we're searching for
maxTweets = 1000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
tweepy_REST_API = dataiku.Folder("tweepy_REST_API")
folder_path = tweepy_REST_API.get_path()
fName = folder_path + '/tweets.txt' # We'll store the tweets in a text file.


# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1

tweetCount = 0

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, lang="en")
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId, lang="en")
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1), lang="en")
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId, lang="en")
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                        '\n')
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Recipe outputs
2o8awzsk = dataiku.Folder("2o8aWzsk")
2o8awzsk_info = 2o8awzsk.get_info()