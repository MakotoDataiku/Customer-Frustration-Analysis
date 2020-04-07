# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from nltk.stem import WordNetLemmatizer
from aspect_clustering.vector_dist import vector_dist
from run_extraction.init_spacy import init_spacy

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Read recipe inputs
aspect_sentiment_pairs = dataiku.Dataset("aspect_sentiment_pairs")
df = aspect_sentiment_pairs.get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df.head()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
lemmatizer = WordNetLemmatizer()
df['noun_lemmatized'] = df.noun.str.lower().apply(lemmatizer.lemmatize)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df_grouped = df.groupby(["product_id", 'noun_lemmatized']).agg({'product_id':'size',
                                                                "polarity_nltk":'mean',
                                                                "polarity_textblob":'mean',
                                                                "review_id":"unique"}).rename(columns={'product_id':'count',
                                                                                                             'polarity_nltk':'mean_polarity_nltk',
                                                                                                             'polarity_textblob':'mean_polarity_textblob'}).reset_index()
df_grouped

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
print("There are %d nouns extracted" %(df_grouped.shape[0]))

punctuality_vec = nlp('punctuality').vector
food_vec = nlp('food').vector
luggage_vec = nlp('luggage').vector
staff_vec = nlp('staff').vector

asp_group = []
for aspect in df_grouped.noun_lemmatized:
    dist_dic = {}
    token_vector = nlp(aspect).vector
    dist_dic['punctuality'] = vector_dist(token_vector, punctuality_vec)
    dist_dic['food'] = vector_dist(token_vector, food_vec)
    dist_dic['luggage'] = vector_dist(token_vector, luggage_vec)
    dist_dic['staff'] = vector_dist(token_vector, staff_vec)
    # group = min([dist_punc, dist_food, dist_lugg, dist_staf])
    max_key = max(dist_dic, key=dist_dic.get)
    asp_group.append(max_key)
df_grouped['group'] = asp_group
df_grouped.loc[df_grouped.noun_lemmatized.str.lower() == prod_id.lower(), "group"] = "company"

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

aspect_sentiment_prep_df = df_grouped # For this sample code, simply copy input to output

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Write recipe outputs
aspect_sentiment_prep = dataiku.Dataset("aspect_sentiment_prep")
aspect_sentiment_prep.write_with_schema(aspect_sentiment_prep_df)