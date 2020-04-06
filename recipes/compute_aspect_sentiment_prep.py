# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
aspect_sentiment_pairs = dataiku.Dataset("aspect_sentiment_pairs")
aspect_sentiment_pairs_df = aspect_sentiment_pairs.get_dataframe()


# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

aspect_sentiment_prep_df = aspect_sentiment_pairs_df # For this sample code, simply copy input to output


# Write recipe outputs
aspect_sentiment_prep = dataiku.Dataset("aspect_sentiment_prep")
aspect_sentiment_prep.write_with_schema(aspect_sentiment_prep_df)
