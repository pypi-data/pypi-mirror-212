import jieba
import jieba.posseg as pseg
import os

def get_stopwords(stopwords_path=""):
    if stopwords_path=='':
        stopwords_path=os.path.join(os.path.dirname(__file__),"data","hit_stopwords.txt")
    stopwords = [w.strip() for w in open(stopwords_path, 'r', encoding='utf-8').readlines()
                 if w.strip() != ""]
    return stopwords

def get_meaningful_words(doc,pos_tags=None,stopwords=None):
    if pos_tags is None:
        pos_tags=['n',  'nr1','nr2','nrj','nrf','nsf',  'nt', 'nz', 'nl','ng','v','vn', 'vd','nd', 'nh', 'nl', 'i','x','a','ad']
    if stopwords is None:
        stopwords=[]
    list_words = pseg.cut(doc)
    list_w = []
    for w, f in list_words:
        # print(w,f)
        if f in pos_tags:
            if w not in stopwords and len(w) != 1:
                list_w.append(w)
    return list_w

