# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
tweet_lufthansa_prepared = dataiku.Dataset("tweet_lufthansa_prepared")
tweet_lufthansa_prepared_df = tweet_lufthansa_prepared.get_dataframe()


# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

lufthansa_no_url_df = tweet_lufthansa_prepared_df # For this sample code, simply copy input to output


# Write recipe outputs
lufthansa_no_url = dataiku.Dataset("lufthansa_no_url")
lufthansa_no_url.write_with_schema(lufthansa_no_url_df)
