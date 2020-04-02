# Python script for extracting aspects based on dependancy rules
#! /usr/bin/env python


import requests
import os
import csv
import numpy as np
import pandas as pd
import urllib.request
import gzip
import sys
import spacy
import json
import boto3
from boto.s3.connection import S3Connection

#import enchant
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

BASE_PATH = os.getcwd()
PARENT = os.path.dirname(BASE_PATH)
CRED_PATH = BASE_PATH + "/data/credentials.txt"

#USE THIS FOR IMPORTING ANY FUNCTIONS FROM src
sys.path.insert(0,BASE_PATH)
import clean_data

prod_pronouns = ['it','this','they','these']


def apply_extraction(row, nlp, sid, text_column, review_id, product_id):
    review_body = row[text_column]
    review_id = row[review_id]
    # review_marketplace = row['marketplace']
    # customer_id = row['customer_id']
    product_id = row[product_id]
    # product_parent = row['product_parent']
    # product_title = row['product_title']
    # product_category = row['product_category']
    # date = str(row['review_date'])
    # star_rating = row['star_rating']
    # url = add_amazonlink(product_id)



    doc=nlp(review_body)


    ## FIRST RULE OF DEPENDANCY PARSE -
    ## M - Sentiment modifier || A - Aspect
    ## RULE = M is child of A with a relationshio of amod
    rule1_pairs = []
    for token in doc:
        A = "999999"
        M = "999999"
        if token.dep_ == "amod" and not token.is_stop:
            M = token.text
            A = token.head.text

            # add adverbial modifier of adjective (e.g. 'most comfortable headphones')
            M_children = token.children
            for child_m in M_children:
                if(child_m.dep_ == "advmod"):
                    M_hash = child_m.text
                    M = M_hash + " " + M
                    break

            # negation in adjective, the "no" keyword is a 'det' of the noun (e.g. no interesting characters)
            A_children = token.head.children
            for child_a in A_children:
                if(child_a.dep_ == "det" and child_a.text == 'no'):
                    neg_prefix = 'not'
                    M = neg_prefix + " " + M
                    break

        if(A != "999999" and M != "999999"):
            if A in prod_pronouns :
                A = "product"
            dict1 = {"noun" : A, 
                     "adj" : M, 
                     "rule" : 1, 
                     "polarity_nltk" : sid.polarity_scores(M)['compound'],
                     "polarity_textblob" : TextBlob(M).sentiment.polarity}
            rule1_pairs.append(dict1)

    ## SECOND RULE OF DEPENDANCY PARSE -
    ## M - Sentiment modifier || A - Aspect
    #Direct Object - A is a child of something with relationship of nsubj, while
    # M is a child of the same something with relationship of dobj
    #Assumption - A verb will have only one NSUBJ and DOBJ

    rule2_pairs = []
    for token in doc:
        children = token.children
        A = "999999"
        M = "999999"
        add_neg_pfx = False
        for child in children :
            if(child.dep_ == "nsubj" and not child.is_stop):
                A = child.text
                # check_spelling(child.text)

            if((child.dep_ == "dobj" and child.pos_ == "ADJ") and not child.is_stop):
                M = child.text
                #check_spelling(child.text)

            if(child.dep_ == "neg"):
                neg_prefix = child.text
                add_neg_pfx = True

    if (add_neg_pfx and M != "999999"):
        M = neg_prefix + " " + M

        if(A != "999999" and M != "999999"):
            if A in prod_pronouns :
                A = "product"
            dict2 = {"noun" : A, 
                     "adj" : M, 
                     "rule" : 2, 
                     "polarity_nltk" : sid.polarity_scores(M)['compound'],
                     "polarity_textblob" : TextBlob(M).sentiment.polarity}
            rule2_pairs.append(dict2)


    ## THIRD RULE OF DEPENDANCY PARSE -
    ## M - Sentiment modifier || A - Aspect
    ## Adjectival Complement - A is a child of something with relationship of nsubj, while
    ## M is a child of the same something with relationship of acomp
    ## Assumption - A verb will have only one NSUBJ and DOBJ
    ## "The sound of the speakers would be better. The sound of the speakers could be better" - handled using AUX dependency



    rule3_pairs = []

    for token in doc:

        children = token.children
        A = "999999"
        M = "999999"
        add_neg_pfx = False
        for child in children :
            if(child.dep_ == "nsubj" and not child.is_stop):
                A = child.text
                # check_spelling(child.text)

            if(child.dep_ == "acomp" and not child.is_stop):
                M = child.text

            # example - 'this could have been better' -> (this, not better)
            if(child.dep_ == "aux" and child.tag_ == "MD"):
                neg_prefix = "not"
                add_neg_pfx = True

            if(child.dep_ == "neg"):
                neg_prefix = child.text
                add_neg_pfx = True

        if (add_neg_pfx and M != "999999"):
            M = neg_prefix + " " + M
                #check_spelling(child.text)

        if(A != "999999" and M != "999999"):
            if A in prod_pronouns :
                A = "product"
            dict3 = {"noun" : A, 
                     "adj" : M, 
                     "rule" : 3, 
                     "polarity_nltk" : sid.polarity_scores(M)['compound'],
                     "polarity_textblob" : TextBlob(M).sentiment.polarity}
            rule3_pairs.append(dict3)

    ## FOURTH RULE OF DEPENDANCY PARSE -
    ## M - Sentiment modifier || A - Aspect

    #Adverbial modifier to a passive verb - A is a child of something with relationship of nsubjpass, while
    # M is a child of the same something with relationship of advmod

    #Assumption - A verb will have only one NSUBJ and DOBJ

    rule4_pairs = []
    for token in doc:


        children = token.children
        A = "999999"
        M = "999999"
        add_neg_pfx = False
        for child in children :
            if((child.dep_ == "nsubjpass" or child.dep_ == "nsubj") and not child.is_stop):
                A = child.text
                # check_spelling(child.text)

            if(child.dep_ == "advmod" and not child.is_stop):
                M = child.text
                M_children = child.children
                for child_m in M_children:
                    if(child_m.dep_ == "advmod"):
                        M_hash = child_m.text
                        M = M_hash + " " + child.text
                        break
                #check_spelling(child.text)

            if(child.dep_ == "neg"):
                neg_prefix = child.text
                add_neg_pfx = True

        if (add_neg_pfx and M != "999999"):
            M = neg_prefix + " " + M

        if(A != "999999" and M != "999999"):
            if A in prod_pronouns :
                A = "product"
            dict4 = {"noun" : A, 
                     "adj" : M, 
                     "rule" : 4, 
                     "polarity_nltk" : sid.polarity_scores(M)['compound'],
                     "polarity_textblob" : TextBlob(M).sentiment.polarity}
            rule4_pairs.append(dict4)


    ## FIFTH RULE OF DEPENDANCY PARSE -
    ## M - Sentiment modifier || A - Aspect

    #Complement of a copular verb - A is a child of M with relationship of nsubj, while
    # M has a child with relationship of cop

    #Assumption - A verb will have only one NSUBJ and DOBJ

    rule5_pairs = []
    for token in doc:
        children = token.children
        A = "999999"
        buf_var = "999999"
        for child in children :
            if(child.dep_ == "nsubj" and not child.is_stop):
                A = child.text
                # check_spelling(child.text)

            if(child.dep_ == "cop" and not child.is_stop):
                buf_var = child.text
                #check_spelling(child.text)

        if(A != "999999" and buf_var != "999999"):
            if A in prod_pronouns :
                A = "product"
            dict5 = {"noun" : A, 
                     "adj" : token.text, 
                     "rule" : 5, 
                     "polarity_nltk" : sid.polarity_scores(token.text)['compound'],
                     "polarity_textblob" : TextBlob(token.text).sentiment.polarity}
            rule5_pairs.append(dict5)


    ## SIXTH RULE OF DEPENDANCY PARSE -
    ## M - Sentiment modifier || A - Aspect
    ## Example - "It ok", "ok" is INTJ (interjections like bravo, great etc)


    rule6_pairs = []
    for token in doc:
        children = token.children
        A = "999999"
        M = "999999"
        if(token.pos_ == "INTJ" and not token.is_stop):
            for child in children :
                if(child.dep_ == "nsubj" and not child.is_stop):
                    A = child.text
                    M = token.text
                    # check_spelling(child.text)

        if(A != "999999" and M != "999999"):
            if A in prod_pronouns :
                A = "product"
            dict6 = {"noun" : A, 
                     "adj" : M, 
                     "rule" : 6, 
                     "polarity_nltk" : sid.polarity_scores(M)['compound'],
                     "polarity_textblob" : TextBlob(M).sentiment.polarity}
            rule6_pairs.append(dict6)


    ## SEVENTH RULE OF DEPENDANCY PARSE -
    ## M - Sentiment modifier || A - Aspect
    ## ATTR - link between a verb like 'be/seem/appear' and its complement
    ## Example: 'this is garbage' -> (this, garbage)

    rule7_pairs = []
    for token in doc:
        children = token.children
        A = "999999"
        M = "999999"
        add_neg_pfx = False
        for child in children :
            if(child.dep_ == "nsubj" and not child.is_stop):
                A = child.text
                # check_spelling(child.text)

            if((child.dep_ == "attr") and not child.is_stop):
                M = child.text
                #check_spelling(child.text)

            if(child.dep_ == "neg"):
                neg_prefix = child.text
                add_neg_pfx = True

        if (add_neg_pfx and M != "999999"):
            M = neg_prefix + " " + M

        if(A != "999999" and M != "999999"):
            if A in prod_pronouns :
                A = "product"
            dict7 = {"noun" : A, 
                     "adj" : M, 
                     "rule" : 7, 
                     "polarity_nltk" : sid.polarity_scores(M)['compound'],
                     "polarity_textblob" : TextBlob(M).sentiment.polarity}
            rule7_pairs.append(dict7)



    aspects = []

    aspects = rule1_pairs + rule2_pairs + rule3_pairs +rule4_pairs +rule5_pairs + rule6_pairs + rule7_pairs

    # replace all instances of "it", "this" and "they" with product_id
    # aspects = [(A,M,P1,P2,r) if A not in prod_pronouns else (product_id,M,P1,P2,r) for A,M,P1,P2,r in aspects ]
    
    dic = {"review_id" : review_id , 
           "aspect_pairs" : aspects, 
           # "review_marketplace" : review_marketplace,
           # "customer_id" : customer_id, 
           "product_id" : product_id, 
           # "product_parent" : product_parent,
           # "product_title" : product_title, 
           # "product_category" : product_category, 
           # "date" : date, 
           # "star_rating" : star_rating, 
           # "url" : url
          }

    return dic


def extract_aspects(reviews,nlp,sid, text_column, review_id, product_id):

    #reviews = df[['review_id', 'review_body']]
    # nlp = init_spacy()
    # sid = init_nltk()

    print("Entering Apply function!")
    aspect_list = reviews.apply(lambda row: apply_extraction(row,nlp,sid, 
                                                             text_column, 
                                                             review_id, 
                                                             product_id), axis=1) #going through all the rows in the dataframe

    return aspect_list


def aspect_extraction(nlp, sid, arg, csvname, tsvname, text_column, review_id, product_id, folder_path):
    usecols =  ['review_id','review_body','product_id']
    reviews = data
    if reviews.shape[0]>1000000:
        reviews = reviews.sample(n=1000, random_state=222)
        print("Since review data frame was too big, sample has been taken")
    else:
        reviews = reviews
    reviews = clean_data.clean_data(reviews, text_column = text_column)
    aspect_list = extract_aspects(reviews,nlp,sid, text_column, review_id, product_id)
    aspect_list = list(aspect_list)
    json_path = folder_path + "/reviews_aspect_raw.json"
    with open(json_path, 'w') as outfile:
        json.dump(aspect_list, outfile)
    #reviews = pd.concat([reviews,chunk])

    #print(f'Shape of the merged file:{reviews.shape}')



    return 1

if __name__ == '__main__' :
    # nlp = init_spacy()
    a = aspect_extraction(nlp, sid)

    # USE THIS IF YOU WANT TO SEE THE ASPECTS IN A FILE
    # with open('your_file.txt', 'w') as f:
    #     for item in a:
    #         f.write("%s\n" % item)
