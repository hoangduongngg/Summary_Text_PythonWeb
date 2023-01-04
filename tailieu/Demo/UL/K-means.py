import os
from gensim.models import KeyedVectors
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import gensim
import pandas as pd

def chuanHoaCau(sentences):
    temp=[]
    for i in sentences:
        i=gensim.utils.simple_preprocess(i)
        i=' '.join(i)
        if i!='':
            temp.append(i)
    return temp       

def createSummary(content):
    path_w2v=os.getcwd()+"\\UL\\Pre_train_w2v"
    content_parsed=content.lower()
    content_parsed=content_parsed.replace('\n', '. ')
    content_parsed=content_parsed.strip()
    sentences=content_parsed.split('.')
    sentences=chuanHoaCau(sentences)
    w2v=KeyedVectors.load_word2vec_format(path_w2v+"/wiki.vi.model.bin", binary=True)
    vocab=w2v.vocab
    X=[]
    for sentence in sentences:
        words=sentence.split(" ")
        sentence_vec=np.zeros((400))
        count=0
        for word in words:
            if word in vocab:
                sentence_vec+=w2v[word]
        X.append(sentence_vec)
    n_clusters=4
    kmeans=KMeans(n_clusters=n_clusters)
    kmeans.fit(X)
    avg=[]
    for i in range(n_clusters):
        idx=np.where(kmeans.labels_==i)[0]
        avg.append(np.mean(idx))
    closest, _=pairwise_distances_argmin_min(kmeans.cluster_centers_, X)
    ordering=sorted(range(n_clusters), key=lambda k: avg[k])
    summary='. '.join([sentences[closest[idx]].capitalize() for idx in ordering])
    summary+='.'
    return summary

data=pd.read_csv("UL\Data\data.csv")
origin_summary=[]
summaries=[]
for i in range(0, 500):
    try:
        summaries.append(createSummary(data['Nội dung'][i]))
        origin_summary.append(data['Tóm tắt'][i])
    except:
        summaries.append(data['Nội dung'][i])
        origin_summary.append(data['Tóm tắt'][i])
        print(i)
df=pd.DataFrame({'summary':summaries, 'origin summary':origin_summary})
df.to_csv(os.getcwd()+'\\UL\\kM.csv')