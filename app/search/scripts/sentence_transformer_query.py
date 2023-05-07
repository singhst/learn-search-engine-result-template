import sys,re,glob,os,time
from bs4 import BeautifulSoup
from sqlitedict import SqliteDict
from urllib.parse import urljoin
import numpy as np
import nltk
from nltk import word_tokenize, pos_tag
from nltk.stem import PorterStemmer
from collections import OrderedDict,Counter
from math import log,sqrt
sys.setrecursionlimit(10000)
ps = PorterStemmer()
nltk.download('punkt')

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')


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

# put stopwords in same folder
stopword_file = open("./stopwords.txt")
stopwords = set([rows.rstrip('\n') for rows in stopword_file])

def reformat_result(original_results: list):
    query_results = []
    for page in original_results:
        score, title, url_full, last_modified_date, size, word_freq_list_top_5, parent, child, pageID = page
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


def extract_stemmed_word(textList,stopwordList = stopwords):
    res = [word.lower() for word in textList] # convert to lower case
    res = [re.sub('[^a-z0-9 ]+', '', w) for w in res]
    res = [re.sub('\s+', ' ', w) for w in res]
    res = [s.strip() for s in res] 
    res = [w for w in res if len(w)>0] 
    res = [w for w in res if w not in stopwordList] # remove stopwords
    res = [ps.stem(w) for w in res] # stemming using porter algorithm with nltk library
    return res
def cosSim(a,b):
    return np.sum(a*b)/(np.sqrt(np.sum(a**2))*np.sqrt(np.sum(b**2)))
def query_token(query_text):
    res = re.findall(r'"(.*?)"', query_text) # get the string in quotation
    unigrams = word_tokenize(query_text)
    res.extend(unigrams)
    res = extract_stemmed_word(res)
    return res
def get_title_cosine(querylist):
    score = {}
    for q in querylist:
        try:
            qid = title_word_to_wordID[q]
        except:
            # print(f"{q} is not indexed in title")
            continue
        postingList = title_inverted_index[qid] #[docId, tfidf_title]
        for post in postingList:
            if post[0] not in list(score.keys()):
                score[post[0]] = post[1]
            else:
                score[post[0]] += post[1]
    for k,v in score.items():
        score[k] = v/title_norm[k]/sqrt(len(querylist))
    return score

def get_body_cosine(querylist):
    score = {}
    for q in querylist:
        try:
            qid = body_word_to_wordID[q]
        except:
            # print(f"{q} is not indexed in body")
            continue
        postingList = body_inverted_index[qid] #[docId,tf , tfidf_title]
        for post in postingList:
            if post[0] not in list(score.keys()):
                score[post[0]] = post[2]
            else:
                score[post[0]] += post[2]
    for k,v in score.items():
        score[k] = v/body_norm[k]/sqrt(len(querylist))
    return score
def getPageInfo(docID):
    pageDetails = pageID_details[docID]
    words,tfs = list(pageDetails[3].keys()),list(pageDetails[3].values()) 
    top5_tfsPosititon = sorted(range(len(tfs)),key=lambda x:tfs[x],reverse=True)[:5]
    top5_words = list(np.array(words)[top5_tfsPosititon])
    top5_tfs = list(np.array(tfs)[top5_tfsPosititon])
    return [
        pageDetails[0], #pageTitle
        pageID_to_url[docID], #url
        pageDetails[1], #lastModified
        pageDetails[2], #size
        [[top5_words[i],top5_tfs[i]] for i in range(5)],
        [pageID_to_url[pid] for pid in pageID_to_parentID[docID]],
        [pageID_to_url[pid] for pid in pageDetails[4]]    
    ]

def process_query(query_text):
    if query_text[:12]!="SENT_SEARCH:":
        querylist = query_token(query_text)
        print(">>> sentence_transformer | process_query() | querylist: {}".format(querylist))
        titleSim = get_title_cosine(querylist)
        bodySim = get_body_cosine(querylist)
        titleBoostedSim = {}
        matchTitle,matchBody = set(titleSim.keys()),set(bodySim.keys())
        for k in matchTitle.union(matchBody):
            if k in matchTitle.intersection(matchBody):
                titleBoostedSim[k] = 0.7 * titleSim[k] + bodySim[k]
            else:
                titleBoostedSim[k] = titleSim.get(k,0) + bodySim.get(k,0)
        scores = list(titleBoostedSim.values())
        docIDs = list(titleBoostedSim.keys())
        n_page = 50
        topScoresPosition = [sorted(range(len(scores)),key=lambda x:scores[x],reverse=True)]
        topScore = list(np.array(scores)[topScoresPosition])[:n_page]
        topPages = list(np.array(docIDs)[topScoresPosition])[:n_page]
        res = [[topScore[i],*getPageInfo(int(topPages[i])),topPages[i]] for i in range(len(topPages))]
        return reformat_result(res)
    else:
        query_sent = query_text[12:]
        query_emb = model.encode(query_sent)
        n_clus = len(list(centroid_dict.keys()))
        clus_sim = []
        for i in range(n_clus):
            clus_sim.append([i, cosSim(query_emb,centroid_dict[i])])

        top_clusters = sorted(clus_sim,key=lambda x:x[1],reverse=True)[:10]
        top_clusters = [x[0] for x in top_clusters]
        sent_query_res = []
        for clus in top_clusters:
            sentIdList = clusToSentId[clus]
            for sentId in sentIdList:
                sentId = int(sentId)
                sent_query_res.append([sentId,SentIdToPageid[sentId],SentIdToSent[sentId],cosSim(query_emb,SentIdToEmbedding[sentId])])
        res = sorted(sent_query_res,key = lambda x:-x[3])[:50] # in [sentId, pageId, Sentence, cosSim]
        # print(res)
        res = [[res[i][3],*getPageInfo(res[i][1]),res[i][1]] for i in range(len(res))] #is it posible to show the sentence in frontend?
        return reformat_result(res)

def getTop5_FreqWord(pageID):
    pageDetails = pageID_details[pageID]
    words,tfs = list(pageDetails[3].keys()),list(pageDetails[3].values()) 
    top5_tfsPosititon = sorted(range(len(tfs)),key=lambda x:tfs[x],reverse=True)[:5]
    top5_words = list(np.array(words)[top5_tfsPosititon])
    return top5_words


if __name__=="__main__":
    query_text = "SENT_SEARCH: The British government acknowledges that it must take actions beyond addressing its domestic audience."
    results = process_query(query_text)
    print(">>> main | #results: {} | results: {}".format(len(results), results))