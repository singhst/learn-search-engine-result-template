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

print(invertedIndex[1])
