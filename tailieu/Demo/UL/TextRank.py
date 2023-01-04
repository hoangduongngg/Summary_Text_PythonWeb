import numpy as np
import pandas as pd
import nltk
import re
from gensim.models import KeyedVectors
import networkx as nx
import gensim
import os
from sklearn.metrics.pairwise import cosine_similarity

#one time execution
#nltk.download('punkt')

def chuanHoaCau(sentences):
    temp=[]
    for i in sentences:
        i=gensim.utils.simple_preprocess(i)
        i=' '.join(i)
        if i!='':
            temp.append(i)
    return temp

def createSummary(content):
    content_parsed=content.lower()
    content_parsed=content_parsed.replace('\n', '. ')
    content_parsed=content_parsed.strip()
    sentences=content_parsed.split('.')
    sentences=chuanHoaCau(sentences)
    w2v=KeyedVectors.load_word2vec_format(os.getcwd()+"\\UL\\Pre_train_w2v\\wiki.vi.model.bin", binary=True)
    vocab=w2v.vocab
    words = list(w2v.wv.index_to_key)
    X=[]
    for sentence in sentences:
        words=sentence.split(" ")
        sentence_vec=np.zeros((400))
        count=0
        for word in words:
            if word in vocab:
                sentence_vec+=w2v[word]
                count+=1
        X.append(sentence_vec/(float(count)))
    sim_mat=np.zeros([len(sentences), len(sentences)])
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i!=j:
                sim_mat[i][j]=cosine_similarity(X[i].reshape(1, 400), X[j].reshape(1, 400))[0,0]
    nx_graph=nx.from_numpy_array(sim_mat)
    scores=nx.pagerank(nx_graph)
    ranked_sentences=sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
    summary='. '.join([ranked_sentences[i][1].capitalize() for i in range(0, 4)])
    summary+='.'
    return summary

data=pd.read_csv("UL\Data\data.csv")
data.drop_duplicates(subset=['Nội dung'], inplace=True)
data.dropna(axis=0, inplace=True)
#Danh sách bản tóm tắt
summaries=[]
for i in range(0, 3000):
    summaries.append(createSummary(data['Nội dung'][i]))
df=pd.DataFrame({'summary':summaries,'origin summary':data['Tóm tắt']})
path=os.getcwd()
df.to_csv(path+'\\UL\\textRank.csv')
