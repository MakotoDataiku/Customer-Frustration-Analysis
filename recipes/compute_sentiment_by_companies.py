# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
aspects_grouped = dataiku.Dataset("aspects_grouped")
aspects_grouped_df = aspects_grouped.get_dataframe()


# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

sentiment_by_companies_df = aspects_grouped_df # For this sample code, simply copy input to output


# Write recipe outputs
sentiment_by_companies = dataiku.Dataset("sentiment_by_companies")
sentiment_by_companies.write_with_schema(sentiment_by_companies_df)
