# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
tweets_noURL = dataiku.Dataset("tweets_noURL")
tweets_noURL_df = tweets_noURL.get_dataframe()




# Write recipe outputs
aspect_sentiment_pairs = dataiku.Folder("lgDPtGGq")
aspect_sentiment_pairs_info = aspect_sentiment_pairs.get_info()
