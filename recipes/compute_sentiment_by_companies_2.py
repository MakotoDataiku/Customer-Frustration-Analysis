# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Read recipe inputs
aspects_grouped = dataiku.Dataset("aspect_sentiment_categorised")
df = aspects_grouped.get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def weighted_ave(x):
    d = {}
    d['weighted_ave_nltk'] = (x["mean_polarity_nltk"] * x["count"]).sum() / x["count"].sum()
    d['weighted_ave_tb'] = (x["mean_polarity_textblob"] * x["count"]).sum() / x["count"].sum()
    return pd.Series(d, index=['weighted_ave_nltk', 'weighted_ave_tb'])

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df_grouped = df.groupby(["product_id", "group"]).apply(weighted_ave).reset_index()
df_clustered = df.groupby(["product_id", "k_means_clusters"]).apply(weighted_ave).reset_index()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

sentiment_by_companies_df = df_grouped # For this sample code, simply copy input to output

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Write recipe outputs
sentiment_by_companies = dataiku.Dataset("Cat_analysis_by_companies")
sentiment_by_companies.write_with_schema(df_grouped)

KM_analysis_by_companies = dataiku.Dataset("KM_analysis_by_companies")
KM_analysis_by_companies.write_with_schema(df_clustered)