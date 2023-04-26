from typing import List, Dict, Union
import math
from sqlitedict import SqliteDict

import re
from string import punctuation
import nltk
from nltk import word_tokenize, pos_tag
from nltk.stem import PorterStemmer
ps = PorterStemmer()
nltk.download('punkt')

## load stopwords
stopword_file = open("./stopwords.txt")
stopwords = set([rows.rstrip('\n') for rows in stopword_file])
print("stopwords:", stopwords)  # for checking


# read dictionaries
url_to_pageID = SqliteDict('./app/db/url_to_pageID.sqlite')
pageID_to_url = SqliteDict('./app/db/pageID_to_url.sqlite')

# page body
body_forward_index = SqliteDict('./app/db/body_forward_index.sqlite')
body_inverted_index = SqliteDict('./app/db/body_inverted_index.sqlite')
body_word_to_wordID = SqliteDict('./app/db/body_word_to_wordID.sqlite')
body_wordID_to_word = SqliteDict('./app/db/body_wordID_to_word.sqlite')
body_norm = SqliteDict('./app/db/body_norm.sqlite')

# page title
title_forward_index = SqliteDict('./app/db/title_forward_index.sqlite')
title_inverted_index = SqliteDict('./app/db/title_inverted_index.sqlite')
title_word_to_wordID = SqliteDict('./app/db/title_word_to_wordID.sqlite')
title_wordID_to_word = SqliteDict('./app/db/title_wordID_to_word.sqlite')
title_norm = SqliteDict('./app/db/title_norm.sqlite')

# others
pageID_to_parentID = SqliteDict('./app/db/pageID_to_parentID.sqlite')
pageID_details = SqliteDict('./app/db/pageID_details.sqlite')


## handling query
# split query for pharse with quotation marks
def split_query_quot(queries):
    reg_exp_quot = re.compile("\"(?:\w+(?: )?)+\"|\w+")
    matched_reg = re.findall(reg_exp_quot, queries)
    num_query = len(matched_reg)
    for i in range(num_query):
        if "\"" in matched_reg[i]:
            matched_reg[i] = matched_reg[i].replace("\"", "")
            splits = matched_reg[i].split()
            matched_reg.extend(splits)
    return matched_reg

# convert splits to string
def split_to_str(splits):
    # str_result = splits[0]
    # for i in range(len(splits)-1):
    #     str_result += " " + splits[i+1]
    return " ".join(splits)

# clean query text
def clean_stem_query (tokens):
    punc_table = str.maketrans('', '', punctuation)    # remove punctuation
    tokens = [w.translate(punc_table) for w in tokens]
    tokens = [word.lower() for word in tokens] # convert to lower case
    tokens = [re.sub('[^A-Za-z0-9\s]+', '', w).strip() for w in tokens]
    tokens = [re.sub('\s+', ' ', w) for w in tokens]
    tokens = [w for w in tokens if w != ''] 
    stop_words = stopwords
    tokens = [w for w in tokens if w not in stop_words] # remove stopwords
    # stemming using porter algorithm with nltk library
    for i in range(len(tokens)):
        if len(tokens[i].split()) == 1: #unigram
            tokens[i] = ps.stem(tokens[i])
        else:
            stemmed_split = [ps.stem(w) for w in tokens[i].split()] #bigram
            tokens[i] = split_to_str(stemmed_split)
    return tokens


def display_query_results(cos_sim_list_result) -> List[Dict[str,Union[int,float,str,dict]]]:
    query_results = []
    for page in cos_sim_list_result:
        pageID , score = page[0] , page[1] 
        # available from pageID_details
        title = pageID_details[pageID][0]
        url_full = pageID_to_url[str(pageID)]
        last_modified_date = pageID_details[pageID][1]
        size = pageID_details[pageID][2]
        word_freq = pageID_details[pageID][3]
        # key words
        word_freq_list = sorted(list(word_freq.items()), key=lambda x: x[1], reverse=True)
        word_freq_list_top_5 = word_freq_list[:5]
        # parent and child
        parentID = pageID_to_parentID[pageID]
        parent = [pageID_to_url[str(p)] for p in parentID]
        childID = pageID_details[pageID][4]
        child = [pageID_to_url[str(c)] for c in childID]
        
        # all_results = [score, title, url_full, pageID,last_modified_date, size, 
        #           word_freq_list_top_5, parent, child]
        all_results = {
            "page_id": pageID,
            "score": score,
            "title": title,
            "url": url_full,
            "last_modification_date": last_modified_date,
            "size_of_page": size,
            "keywords": [{"term": term, "term_freq": term_freq} for term,term_freq in word_freq_list_top_5],
            "parent_links": [{"url": url} for url in parent],
            "child_links": [{"url": url} for url in child],
        }
        query_results.append(all_results)
    return query_results


# retrival function for query
def retrive_func(queries: List[str]):
    # compute for title
    title_query_score = {}
    title_wordID = -1
    for query in queries:
        if query not in title_word_to_wordID.keys():
            print("Word not indexed in title:", query)
            continue
        else:
            title_wordID = title_word_to_wordID[query]
        # retrieve posting list using wordID in page title
        posting_list = title_inverted_index[title_wordID]
        #print(posting_list) # check
        
        # compute accumulated tfidf for query in title
        for page in posting_list:
            pageID , tf_idf = page[0] , page[1]
            if pageID not in title_query_score:
                title_query_score[pageID] = [tf_idf * 1, 1]
            else:
                title_query_score[pageID][0] += tf_idf * 1
                title_query_score[pageID][1] += 1
    cos_sim_title = title_query_score.copy() # cosine sim as compared with title
    
    for pageID, score in title_query_score.items():
        title_norm_cos = title_norm[pageID]
        inner_prod = float(title_query_score[pageID][0])
        query_norm = math.sqrt(title_query_score[pageID][1])
        try:
            cos_sim_title[pageID] = inner_prod / (title_norm_cos * query_norm)
        except ZeroDivisionError:
            print("ZeroDivisionError")
            cos_sim_title[pageID] = 0
    
    # similarly compute for page body
    body_query_score = {}
    body_wordID = -1
    for query in queries:
        if query not in body_word_to_wordID.keys():
            print("Not indexed in page body:", query)
            continue
        else:
            body_wordID = body_word_to_wordID[query]
        # retrieve posting list using wordID in page body
        posting_list = body_inverted_index[body_wordID]
        
        # compute accumulated tfidf for query in page body
        for page in posting_list:
            pageID , tf_idf = page[0] , page[2]
            # compute accumulated tfidf for query in body
            if pageID not in body_query_score:
                body_query_score[pageID] = [tf_idf * 1, 1]
            else:
                body_query_score[pageID][0] += tf_idf * 1
                body_query_score[pageID][1] += 1
    
    cos_sim_body = body_query_score.copy() # cosine sim as compared with page body
    
    for pageID, score in body_query_score.items():
        inner_prod = float(body_query_score[pageID][0])
        doc_norm = body_norm[pageID]
        query_norm = math.sqrt(body_query_score[pageID][1])
        
        try:
            cos_sim_body[pageID] = inner_prod / (query_norm * doc_norm)
        except ZeroDivisionError:
            print("ZeroDivisionError")
            cos_sim_body[pageID] = 0
    
    #########################################################################
    # combine both page title and body
    cos_sim_combined = cos_sim_body.copy()
    for pageID, score in cos_sim_title.items():
        if pageID not in cos_sim_combined:
            cos_sim_combined[pageID] = score * 0.7
        else:
            cos_sim_combined[pageID] = score* 0.7 + cos_sim_combined[pageID]*0.3 #weighted average
    
    # sort and filter top 50 pages for display
    cos_sim_combined_list = list(cos_sim_combined.items())
    cos_sim_list_sorted = sorted(cos_sim_combined_list, key=lambda x: x[1], reverse=True)
    print("No of related pages:" + str(len(cos_sim_list_sorted)))
    cos_sim_list_sorted_filter = cos_sim_list_sorted[:50]
    
    # display desired format
    result = display_query_results(cos_sim_list_sorted_filter)
    return result


def getTop5_FreqWord(pageID):
    word_freq = pageID_details[pageID][3]
    word_freq_list_sorted = sorted(list(word_freq.items()), key=lambda x: x[1], reverse=True)
    top_five_word = [w[0] for w in word_freq_list_sorted[:5]]
    return top_five_word


def reformulate(original_results):
    reformulated = []
    for ori_result in original_results:
        pageID = ori_result["index"]
        similarity_combined = ori_result["title_sim"] + ori_result["body_sim"]
        reformulated.append([pageID, similarity_combined])
    reformulated_sort = sorted(reformulated, key=lambda x: x[1], reverse=True)
    result = display_query_results(reformulated_sort)
    return result
