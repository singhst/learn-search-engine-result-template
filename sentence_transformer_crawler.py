import sys,re,glob,os,requests,pickle,time
from bs4 import BeautifulSoup
from sqlitedict import SqliteDict
from urllib.parse import urljoin
from datetime import datetime
import numpy as np
import nltk
from nltk import word_tokenize, pos_tag
from nltk.stem import PorterStemmer
from collections import OrderedDict,Counter
from math import log,sqrt
sys.setrecursionlimit(10000)
ps = PorterStemmer()
nltk.download('punkt')

# put stopwords in same folder
stopword_file = open("stopwords.txt")
stopwords = set([rows.rstrip('\n') for rows in stopword_file])
def extract_stemmed_word(document,stopwordList = stopwords):
    res = word_tokenize(document) # tokenization
    res = [word.lower() for word in res] # convert to lower case
    res = [re.sub('[^a-z0-9]+', '', w) for w in res] 
    res = [w for w in res if len(w)>0] 
    res = [w for w in res if w not in stopwordList] # remove stopwords
    res = [ps.stem(w) for w in res] # stemming using porter algorithm with nltk library
    return res,[" ".join(bigram) for bigram in nltk.bigrams(res)]

if __name__=="__main__":

    path_data = "data"
    path_db = "app/db"

    if not os.path.exists(path_data):
        os.makedirs(path_data)
    if not os.path.exists(path_db):
        os.makedirs(path_db)




    # Initialize OrderedDict
    # url -> pageID, pageID -> url
    url_to_pageID,pageID_to_url = OrderedDict(),OrderedDict()
    # Body text : word -> wordID//wordId -> word//forward index//inverted index
    body_word_to_wordID, body_wordID_to_word, body_forward_index, body_inverted_index = OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict()
    # Title text : word -> wordID//wordId -> word//forward index//inverted index
    title_word_to_wordID, title_wordID_to_word, title_forward_index, title_inverted_index = OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict()
    # PageId->(page title, last modified date, size of page, word freq dictionary and child pageIds)
    # PageId->ParentID
    pageID_details, pageID_to_parentID = OrderedDict(),OrderedDict()
    # Store the L2-Norm of tfidf on each doc & title
    body_norm,title_norm = OrderedDict(),OrderedDict()


    page = "https://www.cse.ust.hk/~kwtleung/COMP4321/"
    origin = "testpage.htm"

    re_clean = r'[\r\n\t]'

    def get_hyperlink(soup,cur_url):
        soup_a = soup.find_all("a")
        return [(re.sub(re_clean,'',a.text),urljoin(cur_url,a.get("href"))) for a in soup_a]

    def get_lastModified(headers):
        # print(headers["Last-Modified"])
        time_str = headers.get("Last-Modified","")
        try:
            return datetime.strptime(time_str[:-4],"%a, %d %b %Y %H:%M:%S").strftime("%Y-%m-%d")
        except:
            return datetime.now().strftime("%Y-%m-%d")    
    def get_doclength(response):
        return int(response.headers.get("Content-Length",len(response.text)))

    # get parent pageId from pageID_details
    def get_parent(pageID,pageID_details):
        res = []
        for k,v in pageID_details.items():
            if (pageID in v[4])&(k<pageID):
                res.append(k)
        return res

    def get_maxtf(docId,forward_index):
        return max(forward_index[docId].values())


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


    html_soup = {}
    pending = [page + origin]
    visited = []
    while len(pending)>0:
        cur_page = pending.pop(0)
        if not(cur_page in visited):
            retry_cnt = 0
            retry_limit = 10
            while (retry_cnt<retry_limit):
                try:
                    response = requests.get(cur_page)
                    retry_cnt = retry_limit
                except:
                    retry_cnt+=1
                    time.sleep(10)
                    print(f"retrying in access the page:{cur_page} : {retry_cnt+1}")
            html_text = response.text
            soup = BeautifulSoup(html_text,"html.parser")
            last_modifiedDate = get_lastModified(response.headers)
            doc_length = get_doclength(response)
            title_text = soup.find("title").text
            soup_text = soup.get_text(" ")
            #initialize the master storage
            html_soup[cur_page] = {}
            child_links = get_hyperlink(soup,cur_page)
            #current page id, sequence base on the visit sequence 
            cur_page_id = len(url_to_pageID)
            pageID_to_url[cur_page_id] = cur_page
            url_to_pageID[cur_page] = cur_page_id

            body_word_token,body_bi_gram = extract_stemmed_word(soup_text)
            title_word_token,title_bi_gram = extract_stemmed_word(title_text)

            body_word_freq = OrderedDict(Counter(body_word_token) + Counter(body_bi_gram))
            # Process body index
            cur_wordid_freq = OrderedDict()
            for k,v in body_word_freq.items():
                if k not in body_word_to_wordID.keys():
                    word_id = len(body_word_to_wordID) #get word id on the order it process
                    body_word_to_wordID[k] = word_id #save word -> id
                    body_wordID_to_word[word_id] = k #save id -> word
                cur_word_id = body_word_to_wordID[k]
                cur_wordid_freq[cur_word_id] = v #convert counter to (wordId -> freq)
                if cur_word_id in body_inverted_index.keys():
                    body_inverted_index[cur_word_id].append([cur_page_id,v])
                else:
                    body_inverted_index[cur_word_id] = [[cur_page_id,v]]
            body_forward_index[cur_page_id] = cur_wordid_freq #save page -> (wordId -> freq)


            
            # Process title index
            title_word_freq = OrderedDict(Counter(title_word_token) + Counter(title_bi_gram))
            cur_wordid_freq = OrderedDict()
            for k,v in title_word_freq.items():
                if k not in title_word_to_wordID.keys():
                    word_id = len(title_word_to_wordID) #get word id on the order it process
                    title_word_to_wordID[k] = word_id #save word -> id
                    title_wordID_to_word[word_id] = k #save id -> word
                cur_word_id = title_word_to_wordID[k]
                cur_wordid_freq[cur_word_id] = v #convert counter to (wordId -> freq)
                if cur_word_id in title_inverted_index.keys():
                    title_inverted_index[cur_word_id].append([cur_page_id])
                else:
                    title_inverted_index[cur_word_id] = [[cur_page_id]]
            title_forward_index[cur_page_id] = [title_word_to_wordID[word] for word in list(title_word_freq.keys())] #save page -> (wordId -> freq)


            cur_page_info = [
                title_text,
                last_modifiedDate,
                doc_length,
                body_word_freq,
                [linkInfo[1] for linkInfo in child_links]
            ]
            pageID_details[cur_page_id] = cur_page_info
            
            html_soup[cur_page] = {
                "link_to" : child_links,
                "soup":soup,
                "text":soup_text,
                # "title_word_token":title_word_token,
                # "title_bi_gram":title_bi_gram,
                # "body_word_token":body_word_token,
                # "body_bi_gram":body_bi_gram,
                # "body_word_freq" : OrderedDict(body_word_freq),
                # "title_word_freq" : OrderedDict(title_word_freq),
                # "last_mondified" : last_modifiedDate,
                "length": doc_length 
            }
            visited.append(cur_page)
            pending+=[link[1] for link in child_links]
            # if cur_page_id%10==0:
            #     print(f"Crawling {cur_page_id} page")
            print(f"Crawling pageId:{cur_page_id} out of {len(set(visited).union(set(pending)))} pages found so far; title:{title_text},last modified:{last_modifiedDate};")
                

    # convert child link urls -> linkId
    for k,v in pageID_details.items():
        child_linkId = []
        for child_link in pageID_details[k][4]:
            child_linkId.append(url_to_pageID[child_link])
        pageID_details[k][4] = child_linkId
    # save parentId: store if cur_id > parentId for simplicity
    for pageID_ in pageID_details.keys():
        pageID_to_parentID[pageID_] = get_parent(pageID_,pageID_details)
        
        
    # body TFIDF
    num_doc = len(pageID_to_url)
    for k,v in body_inverted_index.items():
        # k : wordId -> v : postingList
        # if (k+1)%5000==0:
        #     print(f"processing {k+1}/{len(body_inverted_index)} of body inverted index")
        idf = log(num_doc/len(v),2)
        for posting in v:
            # posting in posting list is stored in [pageId,tf] -> [pageId,tf,tfidf_max]
            docId = posting[0]
            tfidf_max = (posting[1]/get_maxtf(docId,body_forward_index))*idf
            posting.append(tfidf_max)

    # store L2-norm in body_norm
    for k,v in body_forward_index.items():
        # k : docId
        # v store the wordId -> freq in each doc
        tfidf_list = []
        for wid_ in v.keys():
            # Note that for posting(docId,tf,tfidf_max) of a word id, 
            # record exists exactly one time if the word in the doc
            tfidf_wid = list(filter(lambda x:x[0]==k,body_inverted_index[wid_]))[0][2]
            tfidf_list.append(tfidf_wid)
        tfidf_arr = np.array(tfidf_list)
        body_norm[k] = np.linalg.norm(tfidf_arr,ord=2) #compute L2 Norm


    # title TFIDF
    for k,v in title_inverted_index.items():
        idf = log(num_doc/len(v),2)
        for posting in v:
            # posting in posting list is stored in [pageId] -> [pageId,tfidf]
            # title is short text and hence ignore the tf here
            docId = posting[0]
            posting.append(idf)

    # store L2-norm in title_norm
    for k,v in title_forward_index.items():
        # k : docId
        # v store the wordId -> wordId list
        tfidf_list = []
        for wid_ in v:
            # Note that for posting(docId,tfidf_max) of a word id, 
            # record exists exactly one time if the word in the doc
            tfidf_wid = list(filter(lambda x:x[0]==k,title_inverted_index[wid_]))[0][1]
            tfidf_list.append(tfidf_wid)
        tfidf_arr = np.array(tfidf_list)
        title_norm[k] = np.linalg.norm(tfidf_arr,ord=2) #compute L2 Norm



    dbName = ["url_to_pageID","pageID_to_url",
    "body_word_to_wordID","body_wordID_to_word","body_forward_index","body_inverted_index",
    "title_word_to_wordID","title_wordID_to_word","title_forward_index","title_inverted_index",
    "pageID_details","pageID_to_parentID","body_norm","title_norm"]

    for db in dbName:
        path = f"'{path_db}/{db}.sqlite'"
        cmd = f"createDB({db},{path})"
        print(f"Executing line : {cmd}")
        exec(cmd)
        print("================================================================")
        
    with open(path_data+"/html_data.pkl","wb") as f:
        pickle.dump(html_soup,f)
