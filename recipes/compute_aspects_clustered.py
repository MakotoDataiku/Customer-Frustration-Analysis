# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
aspect_sentiment_pairs = dataiku.Folder("lgDPtGGq")
aspect_sentiment_pairs_info = aspect_sentiment_pairs.get_info()


# Compute recipe outputs
# TODO: Write here your actual code that computes the outputs
# NB: DSS supports several kinds of APIs for reading and writing data. Please see doc.

aspects_clustered_df = ... # Compute a Pandas dataframe to write into aspects_clustered


# Write recipe outputs
aspects_clustered = dataiku.Dataset("aspects_clustered")
aspects_clustered.write_with_schema(aspects_clustered_df)
