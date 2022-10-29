import pandas as pd
from src.dao.Seq2SeqDAO import Seq2SeqDAO
from src.models.Seq2Seq import Seq2Seq
from src import app
from flask import render_template, request
from src.dao.DataDAO import DataDAO
import gensim
import numpy as np
from keras.preprocessing.text import Tokenizer
from src.models.VectorTokenizer import VectorTokenizer
from keras_preprocessing.sequence import pad_sequences

@app.route('/admin/retrain', methods=['GET', 'POST'])
def retrainController():
    dataDAO=DataDAO()
    (rate, listSampleTrained, listSampleNoTrain)=dataDAO.getPercentageSampleNew()
    if request.method=="GET":
        return render_template('/server/retrain.html', rate=rate)
    else:
        dataDAO=DataDAO()
        listSample=listSampleTrained+listSampleNoTrain
        retrain(listSample)
        dataDAO.updateSampleNoTrain(listSampleNoTrain)
        (rate, listSampleTrained, listSampleNoTrain)=dataDAO.getPercentageSampleNew()
        return render_template('/server/retrain.html', rate=rate)

def retrain(listSample):
    df=preprocessing(listSample)
    filterText(df)
    x=np.array(df['Nội dung'])
    y=np.array(df['Tóm tắt'])
    xTokenizer=VectorTokenizer()
    xTokenizer.createTokenizer(x, evaluateWork(x))
    yTokenizer=VectorTokenizer()
    yTokenizer.createTokenizer(y, evaluateWork(y))

    x=xTokenizer.getVectorModel().texts_to_sequences(x)
    x=pad_sequences(x, 500, padding='post')

    y=yTokenizer.getVectorModel().texts_to_sequences(y)
    y=pad_sequences(y, 500, padding='post')

    dropNone(x, y)
    seq2Seq=Seq2Seq(500, 60, 100, 300, xTokenizer, yTokenizer)
    seq2Seq.summary()
    seq2Seq.fit(x, y)
    seq2Seq.getModel()
    seqDAO=Seq2SeqDAO()
    seqDAO.saveModel(seq2Seq)
    

def cleanText(text):
    newString=''
    newString=text.lower()
    newString=gensim.utils.simple_preprocess(newString)
    newString=' '.join(newString)
    return newString

def preprocessing(listSample):
    content=[]
    summary=[]
    for i in range(len(listSample)):
        content.append(cleanText(listSample[i].getContent()))
        summary.append(cleanText(listSample[i].getSum()))
    temp=pd.DataFrame({'Nội dung':content, 'Tóm tắt':summary})
    temp.replace('', np.nan, inplace=True)
    temp.dropna(axis=0, inplace=True)
    df=pd.DataFrame({'Nội dung':np.array(temp['Nội dung']),'Tóm tắt':np.array(temp['Tóm tắt'])})
    df['Tóm tắt']=df['Tóm tắt'].apply(lambda x : 'sostok '+ x + ' eostok')
    return df

def filterText(df):
    content=[]
    summary=[]
    for i in range(0, df['Nội dung'].shape[0]):
        if(len(df['Nội dung'][i].split())<=500) and ((len(df['Tóm tắt'][i].split())<=60)):
            content.append(df['Nội dung'][i])
            summary.append(df['Tóm tắt'][i])
    df=(pd.DataFrame({'Nội dung':content, 'Tóm tắt':summary}))

def evaluateWork(x):
    xTokenizer=Tokenizer()
    xTokenizer.fit_on_texts(list(x))
    thresh=4
    cnt=0
    totCnt=0
    freq=0
    totFreq=0
    for key, value in xTokenizer.word_counts.items():
        totCnt=totCnt+1
        totFreq=totFreq+value
        if(value<thresh):
            cnt=cnt+1
            freq=freq+value    
    return totCnt-cnt

def dropNone(x, y):
    ind=[]
    for i in range(len(y)):
        cnt=0
        for j in y[i]:
            if j!=0:
                cnt=cnt+1
        if(cnt==2):
            ind.append(i)

    y=np.delete(y, ind, axis=0)
    x=np.delete(x, ind, axis=0)