from clean_data.clean_data import clean_data

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
