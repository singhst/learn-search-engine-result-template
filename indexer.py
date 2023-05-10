from sqlitedict import SqliteDict
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
import pickle
from collections import  OrderedDict,Counter
import numpy as np
from nltk import sent_tokenize,word_tokenize


model = SentenceTransformer('all-MiniLM-L6-v2')
data_path = "data/"
with open(data_path+"html_data.pkl","rb") as f:
    html_soup = pickle.load(f)
pageID_to_url = SqliteDict('./app/db/pageID_to_url.sqlite')
pageidToSentId,SentIdToPageid,SentIdToSent,SentIdToEmbedding,centroid_dict,clusToSentId = OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict()

import re
re_clean = r'[\r\n\t]'

def createDB(data,db_path,printProgress=True):
    DB = SqliteDict(db_path)
    cnt = 0
    total = len(list(data.keys()))
    for k,v in data.items():
        DB[k] = v
        cnt+=1
        if cnt%1000==0:
            print(f"Inserting {cnt}/{total} to {db_path}")
    DB.commit()
    DB.close()

def cosSim(a,b):
    return np.sum(a*b)/(np.sqrt(np.sum(a**2))*np.sqrt(np.sum(b**2)))

def getSentences(pageId):
    pageText = html_soup[pageID_to_url[pageId]]["soup"].getText("<sep>")
    pageText = [re.sub(re_clean,"",line) for line in pageText.split("<sep>")]
    pageText = [s.strip() for s in pageText if len(s.strip())>0]
    pageText = [". "+s if s[0].isupper() else " "+s for s in pageText]
    cleaned_text = "".join(pageText)
    res = [re.sub("[.]+",".",s) for s in sent_tokenize(cleaned_text)]
    res = [re.sub("[^A-Za-z0-9\s,.!?\'\"]+","",s) for s in res]
    res = [s for s in res if len(word_tokenize(s))>5] # assume a sentence contains at least 3 word
    return res
n_pages = len(list(pageID_to_url.keys()))
sentId = 0
sents_all = []
cnt_sents = Counter()
for i in range(n_pages):
    sents = getSentences(i)
    sents_unique = list(set(sents))
    cnt_sents = cnt_sents + Counter(sents_unique)
    sents_all.append(sents)
sent_usual = [s for s,cnt in list(cnt_sents.items()) if cnt>=20] # get the sentences exists in to many pages

print(len(sents_all))
process_cnt = 0
for sents in sents_all:
    sents = [s for s in sents if s not in sent_usual]  # exclude those sentences
    pageidToSentId[process_cnt] = list(range(sentId,sentId + len(sents)))
    cnt = 0
    if len(sents)>0:
        embs = model.encode(sents)
        embs = embs/np.linalg.norm(embs,axis=1,keepdims=True) # normalized
        for embedding in embs:
            SentIdToPageid[sentId] = process_cnt
            SentIdToEmbedding[sentId] = embedding
            SentIdToSent[sentId] = sents[cnt]
            cnt += 1
            sentId += 1
    if (process_cnt+1)%10==0:
        print(f"processing sentences in page {process_cnt+1} over {n_pages}")
    process_cnt+=1
    

embList = []
for i in range(len(SentIdToEmbedding)):
    embList.append(SentIdToEmbedding[i])
embList = np.array(embList)
# Perform hierarchical clustering on cosine similarities of sentences embeddings
n_clus = 300
clus = AgglomerativeClustering(n_clusters=n_clus,affinity='cosine', linkage='average')
clus.fit(embList)
for i in range(n_clus):
    sentId_cur = np.array(range(len(SentIdToPageid.keys())))[clus.labels_==i]
    centroid_cur = np.mean(embList[sentId_cur],axis=0)
    centroid_dict[i] = centroid_cur
    clusToSentId[i] = sentId_cur
    
    
path_data = "data"
path_db = "app/db"

dbName = ["pageidToSentId","SentIdToPageid","SentIdToSent","SentIdToEmbedding","centroid_dict","clusToSentId"]

for db in dbName:
    path = f"'{path_db}/{db}.sqlite'"
    cmd = f"createDB({db},{path})"
    print(f"Executing line : {cmd}")
    exec(cmd)
    print("================================================================")
