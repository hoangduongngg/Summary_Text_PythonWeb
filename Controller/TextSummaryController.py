from flask import render_template, request
from DAO.Seq2SeqDAO import Seq2SeqDAO
from Model.DataClient import DataClient
from keras_preprocessing.sequence import pad_sequences
import gensim
import requests
from bs4 import BeautifulSoup

def index():
    if request.method=="GET":
        return render_template('/client/index.html', result=None, message=None)
    else:
        content=request.form.get('text')
        if(len(preprocessing(content).split())<60):
            message="Word in content must >= 60"
            return render_template('/client/index.html', result=None, message=message)
        else:
            sum=textSummary(content)
            result=DataClient()
            result.setContent(content)
            result.setSum(sum)
            return render_template('/client/index.html', result=result, message=None)

def textSummaryURL():
    url=request.form.get('text')
    content=getTextURL(url)
    sum=textSummary(content)
    result=DataClient()
    result.setContent(content)
    result.setSum(sum)
    return render_template('/client/index.html', result=result, message=None)

def preprocessing(text):
    newString=''
    newString=text.lower()
    newString=gensim.utils.simple_preprocess(newString)
    newString=' '.join(newString)
    return newString

def textSummary(text):
    textClean=preprocessing(text)
    seq2SeqDAO=Seq2SeqDAO()
    seq2Seq=seq2SeqDAO.getModelPreTrain()
    vectorText=seq2Seq.getXTokenizer().getVectorModel().texts_to_sequences([textClean])
    vectorText=pad_sequences(vectorText, seq2Seq.getMaxTextLen(), padding='post')
    sum=seq2Seq.predrict(vectorText[0])
    return sum
    
def getTextURL(url):
    response=requests.get(url)
    soup=BeautifulSoup(response.content, "html.parser")
    contents=soup.find('div', class_="cms-body detail", id='abody').find_all("p", recursive=False)
    text=''
    for i in contents:
        text+=" "+i.text
    return text