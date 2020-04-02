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