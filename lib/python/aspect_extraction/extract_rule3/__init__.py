def extract_rule3(doc, ner_heads):

    for token in doc:

        children = token.children
        A = "999999"
        M = "999999"
        add_neg_pfx = False
        for child in children :
            if(child.dep_ == "nsubj" and not child.is_stop):
                if child.idx in ner_heads:
                    A = ner_heads[child.idx].text
                else:
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
                A = product_id
            dict3 = {"noun" : A, 
                     "adj" : M, 
                     "rule" : 3, 
                     "polarity_nltk" : sid.polarity_scores(M)['compound'],
                     "polarity_textblob" : TextBlob(M).sentiment.polarity}
            rule3_pairs.append(dict3)
            
    return rule3_pairs