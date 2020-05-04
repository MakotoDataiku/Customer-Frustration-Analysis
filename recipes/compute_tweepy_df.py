# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
tweepy_REST_API = dataiku.Folder("2o8aWzsk")
tweepy_REST_API_info = tweepy_REST_API.get_info()


# Compute recipe outputs
# TODO: Write here your actual code that computes the outputs
# NB: DSS supports several kinds of APIs for reading and writing data. Please see doc.

tweepy_df_df = ... # Compute a Pandas dataframe to write into tweepy_df


# Write recipe outputs
tweepy_df = dataiku.Dataset("tweepy_df")
tweepy_df.write_with_schema(tweepy_df_df)
