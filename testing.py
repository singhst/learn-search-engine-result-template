from sqlitedict import SqliteDict


path_db = "app/db/"
# read dictionaries 
url_to_pageID = SqliteDict(path_db + 'url_to_pageID.sqlite')
pageID_to_url = SqliteDict(path_db + 'pageID_to_url.sqlite')

# page body
body_forward_index = SqliteDict(path_db + 'body_forward_index.sqlite')
body_inverted_index = SqliteDict(path_db + 'body_inverted_index.sqlite')
body_word_to_wordID = SqliteDict(path_db + 'body_word_to_wordID.sqlite')
body_wordID_to_word = SqliteDict(path_db + 'body_wordID_to_word.sqlite')
body_norm = SqliteDict(path_db + 'body_norm.sqlite')

# page title
title_forward_index = SqliteDict(path_db + 'title_forward_index.sqlite')
title_inverted_index = SqliteDict(path_db + 'title_inverted_index.sqlite')
title_word_to_wordID = SqliteDict(path_db + 'title_word_to_wordID.sqlite')
title_wordID_to_word = SqliteDict(path_db + 'title_wordID_to_word.sqlite')
title_norm = SqliteDict(path_db + 'title_norm.sqlite')

# others
pageID_to_parentID = SqliteDict(path_db + 'pageID_to_parentID.sqlite')
pageID_details = SqliteDict(path_db + 'pageID_details.sqlite')

# Enhancement Sentence embedding 


pageidToSentId = SqliteDict(path_db + 'pageidToSentId.sqlite')
SentIdToPageid = SqliteDict(path_db + 'SentIdToPageid.sqlite')
SentIdToSent = SqliteDict(path_db + 'SentIdToSent.sqlite')
SentIdToEmbedding = SqliteDict(path_db + 'SentIdToEmbedding.sqlite')
centroid_dict = SqliteDict(path_db + 'centroid_dict.sqlite')
clusToSentId  = SqliteDict(path_db + 'clusToSentId.sqlite')


if __name__ == "__main__":
    print(">> body_forward_index[:3]: {}".format(body_forward_index[1]))
    print(">> body_inverted_index[:3]: {}".format(body_inverted_index[3]))
    print(">> title_wordID_to_word: {}".format(title_wordID_to_word[5]))
    print(">> title_wordID_to_word: {}".format(title_wordID_to_word[6]))