from sqlitedict import SqliteDict
import math

# Url -> PageID
url2pageID = SqliteDict('./app/db/url2pageID.sqlite')
# PageID -> [PageTitle, LastModified, Size, WordFreqDict, Children]
pageID2Meta = SqliteDict('./app/db/pageID2Meta.sqlite')
# PageID -> [[WordID, frequency]]
forwardIndex = SqliteDict('./app/db/forwardIndex.sqlite')
# PageID -> doc_norm
docNorm = SqliteDict('./app/db/docNorm.sqlite')
# Word -> WordID
word2wordID = SqliteDict('./app/db/word2wordID.sqlite')
# WordID -> [[PageID, frequency]]
invertedIndex = SqliteDict('./app/db/invertedIndex.sqlite')
# Title -> TitleID
title2TitleID = SqliteDict('./app/db/title2TitleID.sqlite')
# PageID -> [TitleID]
forwardIndexTitle = SqliteDict('./app/db/forwardIndexTitle.sqlite')
# TitleID -> [PageID]
invertedIndexTitle = SqliteDict('./app/db/invertedIndexTitle.sqlite')
# PageID -> title_norm
titleNorm = SqliteDict('./app/db/titleNorm.sqlite')
queries = ["comput", "scienc"]
# queries = ["event"]

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
