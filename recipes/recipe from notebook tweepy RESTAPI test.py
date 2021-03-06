# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
import dataiku
from dataiku import pandasutils as pdu
import pandas as pd
import tweepy
from pandas.io.json import json_normalize
import sys
import jsonpickle
import os

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
atoken = "1211674579879391233-VwxwWZO0nnio8wwBVzncqhjfCTmz8S"
asecret = "SUNhejwVlBrsx1B8I7yqXkn9NzjOKR6kzejkAHmJHdOTP"
ckey = "nSLLEuipKq6iJetBCLj33mv1J"
csecret = "s9XGj7t3XMvsmX2EHWeUHex2VvthapZFmmpFAj40VsQV2SvnVg"

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Replace the API_KEY and API_SECRET with your application's key and secret.
auth = tweepy.AppAuthHandler(ckey, csecret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
companies = dataiku.get_custom_variables(typed=True)["company"]

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df = pd.DataFrame()

for company in companies:
    print(company)
    searchQuery = company + " -RT"# this is what we're searching for
    print("search query :", searchQuery)
    maxTweets = 2000 # Some arbitrary large number
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
                    f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')

                    if len(tweet._json['entities']['urls']) == 0:
                        links = ""
                    else:
                        links = tweet._json['entities']['urls'][0]["expanded_url"]

                    if tweet._json["place"]==None:
                        country = ""
                    else:
                        country = tweet._json["place"]['country']

                    if tweet._json["geo"] != None:
                        coordinates = str(tweet._json["geo"]['coordinates'])
                    else:
                        coordinates = ""

                    new_row = pd.DataFrame({'timestamp':tweet._json['created_at'],
                                            'tweet_id':[tweet._json["id"]],
                                            'text':tweet._json["text"],
                                            'hashtags':[tweet._json["entities"]["hashtags"]],
                                            "links":links,
                                            # 'user_mentions':tweet._json["entities"]["user_mentions"][0]["screen_name"],
                                            # 'user_mentions_id':tweet._json["entities"]["user_mentions"][0]["id"],
                                            # 'user_mentions_indices':[tweet._json["entities"]["user_mentions"][0]["indices"]],
                                            'in_reply_to_status_id':tweet._json["in_reply_to_status_id"],
                                            'in_reply_to_user_id':tweet._json["in_reply_to_user_id"],
                                            'in_reply_to_screen_name':tweet._json["in_reply_to_screen_name"],
                                            'user_id':tweet._json["user"]["id"],
                                            'username':tweet._json["user"]["name"],
                                            'screen_name':tweet._json["user"]["screen_name"],
                                            'user_location':tweet._json["user"]["location"],
                                            'followers_count':tweet._json["user"]["followers_count"],
                                            'friends_count':tweet._json["user"]["friends_count"],
                                            'user_creation':tweet._json["user"]["created_at"],
                                            'favourites_count':tweet._json["user"]["favourites_count"],
                                            'coordinates':coordinates,
                                            # 'geo':tweet._json["geo"],
                                            'country':country,
                                            'retweets':tweet._json["retweet_count"],
                                            'retweeted':tweet._json["retweeted"],
                                            'lang':tweet._json["lang"]
                                        })
                    new_row["company"] = company
                    df = df.append(new_row, ignore_index = True)

                tweetCount += len(new_tweets)
                print("Downloaded {0} tweets".format(tweetCount))
                max_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                # Just exit if any error
                print("some error : " + str(e))
                break

    print ("Downloaded {0} tweets for {1}, Saved to {2}".format(tweetCount, company, fName))

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df.head()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
py_recipe_output = dataiku.Dataset("tweepy_REST_API")
py_recipe_output.write_with_schema(df)