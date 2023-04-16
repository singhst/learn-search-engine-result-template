from sqlitedict import SqliteDict
import math

# Url -> PageID
url2pageID = SqliteDict('./app/db/url_to_pageID.sqlite')
# PageID -> [PageTitle, LastModified, Size, WordFreqDict, Children]
pageID2Meta = SqliteDict('./app/db/pageID_details.sqlite')
# PageID -> [[WordID, frequency]]
forwardIndex = SqliteDict('./app/db/body_forward_index.sqlite')
# PageID -> doc_norm
docNorm = SqliteDict('./app/db/body_norm.sqlite')
# Word -> WordID
word2wordID = SqliteDict('./app/db/body_word_to_wordID.sqlite')
# WordID -> [[PageID, frequency]]
invertedIndex = SqliteDict('./app/db/body_inverted_index.sqlite')
# Title -> TitleID
title2TitleID = SqliteDict('./app/db/title_word_to_wordID.sqlite')
# PageID -> [TitleID]
forwardIndexTitle = SqliteDict('./app/db/title_forward_index.sqlite')
# TitleID -> [PageID]
invertedIndexTitle = SqliteDict('./app/db/title_inverted_index.sqlite')
# PageID -> title_norm
titleNorm = SqliteDict('./app/db/title_norm.sqlite')
queries = ["comput", "scienc"]
# queries = ["event"]
# queries = ["test", "page"]


title_score_dict = {}
title_id = -1
for query in queries:
    if query in title2TitleID.keys():
        title_id = title2TitleID[query]
    else:
        print("Title word not indexed:", query)
        continue
    posting_list = invertedIndexTitle[title_id]
    for document in posting_list:
        doc_id = document[0]
        # Pre-computed tf-idf
        tf_idf = document[1]
        # Accumulate the inner product
        if doc_id not in title_score_dict:
            title_score_dict[doc_id] = [tf_idf * 1, 1]
        else:
            title_score_dict[doc_id][0] += tf_idf * 1
            title_score_dict[doc_id][1] += 1
print(title_score_dict)


cos_sim_title = title_score_dict.copy()
for doc_id, score in title_score_dict.items():
    print(">>> doc_id: {}; score: {}".format(doc_id, score))
    word_list = forwardIndexTitle[doc_id]
    print(">>> word_list: {}".format(word_list))
    title_norm = titleNorm[doc_id]
    query_norm = math.sqrt(title_score_dict[doc_id][1])
    inner_prod = float(title_score_dict[doc_id][0])
    cos_sim_title[doc_id] = inner_prod / (title_norm * query_norm)
print("(1)>>> cos_sim_title:", cos_sim_title)
