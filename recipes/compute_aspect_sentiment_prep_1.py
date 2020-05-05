# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from nltk.stem import WordNetLemmatizer
from aspect_clustering.vector_dist import vector_dist
from run_extraction.init_spacy import init_spacy
# from aspect_clustering.add_clusters_to_reviews import add_clusters_to_reviews
from sklearn import cluster
import ast

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Read recipe inputs
aspect_sentiment_pairs = dataiku.Dataset("tweepy_aspect_sentiment_pairs")
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

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df_grouped.head(10)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
print("There are %d nouns extracted" %(df_grouped.shape[0]))

model_path= dataiku.get_custom_variables()['model_path']
nlp = init_spacy(model_path)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
punctuality_vec = nlp('punctuality').vector
food_vec = nlp('food').vector
luggage_vec = nlp('luggage').vector
staff_vec = nlp('staff').vector

companies = df_grouped.product_id.unique()
n_clusters = dataiku.get_custom_variables(typed=True)['NUM_CLUSTERS']
if type(n_clusters) != int:
    n_clusters = ast.literal_eval(n_clusters)
df_vectors = pd.DataFrame()

df_grouped['k_means_clusters'] = np.nan
df_grouped['group'] = np.nan

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
for company in companies:
    df_sub = df_grouped[df_grouped.product_id == company]
    asp_group = []
    asp_vectors = []
    for aspect in df_sub.noun_lemmatized:
        dist_dic = {}
        token_vector = nlp(aspect).vector
        asp_vectors.append(token_vector)
        # df_grouped[df_grouped.noun_lemmatized==aspect, 'noun_vector'] = token_vector
        dist_dic['punctuality'] = vector_dist(token_vector, punctuality_vec)
        dist_dic['food'] = vector_dist(token_vector, food_vec)
        dist_dic['luggage'] = vector_dist(token_vector, luggage_vec)
        dist_dic['staff'] = vector_dist(token_vector, staff_vec)
        # group = min([dist_punc, dist_food, dist_lugg, dist_staf])
        max_key = max(dist_dic, key=dist_dic.get)
        asp_group.append(max_key)

    df_grouped.loc[df_grouped.product_id == company, "group"] = asp_group
    df_grouped.loc[df_grouped.noun_lemmatized.str.lower() == df_grouped.product_id.str.lower(), "group"] = "company"

    df_vectors_sub = pd.DataFrame(asp_vectors)
    df_vectors_sub['product_id'] = company
    df_vectors_sub['noun_lemmatized'] = df_sub['noun_lemmatized'].values
    df_vectors_sub['count'] = df_sub['count'].values

    # -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
    # you have to cluster for each company
    kmeans = cluster.KMeans(n_clusters=n_clusters)
    kmeans.fit(asp_vectors)
    labels = kmeans.labels_
    df_grouped.loc[df_grouped.product_id == company, "k_means_clusters"] = labels
    df_vectors_sub['k_means_clusters'] = labels
    df_vectors = pd.concat([df_vectors, df_vectors_sub])

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df_grouped['k_means_clusters'] = df_grouped.k_means_clusters.astype(int)
df_grouped["tb_importance"] = df_grouped["count"] * df_grouped["mean_polarity_textblob"]

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

# aspect_sentiment_categorised_df = df_grouped # For this sample code, simply copy input to output

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Write recipe outputs
aspect_sentiment_categorised = dataiku.Dataset("tweepy_aspect_sentiment_categorised")
aspect_sentiment_categorised.write_with_schema(df_grouped)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Write recipe outputs
word_vectors = dataiku.Dataset("tweepy_word_vectors")
word_vectors.write_with_schema(df_vectors)