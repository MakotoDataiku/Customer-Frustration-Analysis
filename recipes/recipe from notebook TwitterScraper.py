# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE_MAGIC_CELL
# Automatically replaced inline charts by "no-op" charts
# %pylab inline
import matplotlib
matplotlib.use("Agg")

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
import dataiku
from dataiku import pandasutils as pdu
import pandas as pd
from twitterscraper import query_tweets
import datetime

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
cols = ['screen_name', 'username', 'user_id', 'tweet_id', 'tweet_url', 'timestamp',
           'timestamp_epochs', 'text', 'text_html', 'links', 'hashtags', 'has_media',
           'img_urls', 'video_url', 'likes', 'retweets', 'replies', 'is_replied', 'is_reply_to',
           'parent_tweet_id', 'reply_to_users']

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df = pd.DataFrame(columns=cols)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
company = 'lufthansa'
begindate = datetime.date(2020,1,1)
enddate = datetime.date.today()
list_of_tweets = query_tweets(company,
                          begindate = begindate,
                          enddate = enddate,
                          poolsize = 10)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
for row, tweet in enumerate(list_of_tweets):
    for d in tweet.__dict__:
        df.loc[row,'screen_name'] = tweet.screen_name
        df.loc[row,'username'] = tweet.username
        df.loc[row,'user_id'] = tweet.user_id
        df.loc[row,'tweet_id'] = tweet.tweet_id
        df.loc[row,'tweet_url'] = tweet.tweet_url
        df.loc[row,'timestamp'] = tweet.timestamp
        df.loc[row,'timestamp_epochs'] = tweet.timestamp_epochs
        df.loc[row,'text'] = tweet.text
        df.loc[row,'text_html'] = tweet.text_html
        df.loc[row,'links'] = tweet.links
        df.loc[row,'hashtags'] = tweet.hashtags
        df.loc[row,'has_media'] = tweet.has_media
        df.loc[row,'img_urls'] = tweet.img_urls
        df.loc[row,'video_url'] = tweet.video_url
        df.loc[row,'likes'] = tweet.likes
        df.loc[row,'retweets'] = tweet.retweets
        df.loc[row,'replies'] = tweet.replies
        df.loc[row,'is_replied'] = tweet.is_replied
        df.loc[row,'is_reply_to'] = tweet.is_reply_to
        df.loc[row,'parent_tweet_id'] = tweet.parent_tweet_id
        df.loc[row,'reply_to_users'] = tweet.reply_to_users



# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Recipe outputs
tweet_lufthansa = dataiku.Dataset("tweet_lufthansa")
tweet_lufthansa.write_with_schema(df)