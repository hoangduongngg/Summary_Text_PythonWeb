from statistics import mode
import tensorflow
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from keras.layers import Input, LSTM, Embedding, Dense, Concatenate, TimeDistributed
from keras.models import Model
from keras.callbacks import EarlyStopping
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import gensim
import os

def readData():
    data=pd.read_csv("D:/data.csv")
    data.drop_duplicates(subset=['Nội dung'], inplace=True)
    data.dropna(axis=0, inplace=True)
    return data

def text_cleaner(text):
    newString=''
    newString=text.lower()
    newString=gensim.utils.simple_preprocess(newString)
    newString=' '.join(newString)
    return newString

def clean():
    cleaned_text=[]
    data=readData()
    for t in data['Nội dung']:
        cleaned_text.append(text_cleaner(t))
    cleaned_summary=[]
    for t in data['Tóm tắt']:
        cleaned_summary.append(text_cleaner(t))

    data['cleaned_text']=cleaned_text
    data['cleaned_summary']=cleaned_summary

    data.replace('', np.nan, inplace=True)
    data.dropna(axis=0,inplace=True)
    df=pd.DataFrame({'Nội dung':cleaned_text,'Tóm tắt':cleaned_summary})
    df['Tóm tắt'] = df['Tóm tắt'].apply(lambda x : 'sostok '+ x + ' eostok')
    saveData(df)

def show(data):
    text_word_count=[]
    summary_word_count=[]
    for i in data['cleaned_text']:
        text_word_count.append(len(i.split()))
    for i in data['cleaned_summary']:
        summary_word_count.append(len(i.split()))
    length_df=pd.DataFrame({'text':text_word_count, 'summary':summary_word_count})
    length_df.hist(bins = 30)
    plt.show()
    cnt=0
    for i in data['cleaned_summary']:
        if(len(i.split())<=100):
            cnt=cnt+1
    print(cnt/len(data['cleaned_summary']))
    cnt=0
    for i in data['cleaned_text']:
        if(len(i.split())<=10000):
            cnt=cnt+1
    print(cnt/len(data['cleaned_text']))

def saveData(data):
    path=os.getcwd()
    data.to_csv(path+'\data.csv')

max_text_len=1000
max_summary_len=20
#clean()

def evaluateWork(x_tr):
    x_tokenizer=Tokenizer()
    x_tokenizer.fit_on_texts(list(x_tr))
    thresh=4
    cnt=0
    tot_cnt=0
    freq=0
    tot_freq=0
    for key, value in x_tokenizer.word_counts.items():
        tot_cnt=tot_cnt+1
        tot_freq=tot_freq+value
        if(value<thresh):
            cnt=cnt+1
            freq=freq+value    
    return tot_cnt-cnt

df=pd.read_csv(os.getcwd()+"\data.csv")
x_tr, x_val, y_tr, y_val=train_test_split(np.array(df['Nội dung']), np.array(df['Tóm tắt']), test_size=0.3, random_state=0, shuffle=True) 
x_tokenizer = Tokenizer(num_words=evaluateWork(x_tr))
x_tokenizer.fit_on_texts(list(x_tr))

x_tr_seq=x_tokenizer.texts_to_sequences(x_tr) 
x_val_seq=x_tokenizer.texts_to_sequences(x_val)

x_tr=pad_sequences(x_tr_seq, maxlen=max_text_len, padding='post')
x_val=pad_sequences(x_val_seq, maxlen=max_text_len, padding='post')

x_voc=x_tokenizer.num_words+1

y_tokenizer=Tokenizer(num_words=evaluateWork(y_val)) 
y_tokenizer.fit_on_texts(list(y_tr))
y_tr_seq=y_tokenizer.texts_to_sequences(y_tr) 
y_val_seq=y_tokenizer.texts_to_sequences(y_val) 
y_tr=pad_sequences(y_tr_seq, maxlen=max_summary_len, padding='post')
y_val=pad_sequences(y_val_seq, maxlen=max_summary_len, padding='post')

y_voc=y_tokenizer.num_words+1

ind=[]
for i in range(len(y_tr)):
    cnt=0
    for j in y_tr[i]:
        if j!=0:
            cnt=cnt+1
    if(cnt==2):
        ind.append(i)

y_tr=np.delete(y_tr, ind, axis=0)
x_tr=np.delete(x_tr, ind, axis=0)

ind=[]
for i in range(len(y_val)):
    cnt=0
    for j in y_val[i]:
        if j!=0:
            cnt=cnt+1
    if(cnt==2):
        ind.append(i)

y_val=np.delete(y_val, ind, axis=0)
x_val=np.delete(x_val, ind, axis=0)

latent_dim=300
embedding_dim=200
encoder_inputs=Input(shape=(max_text_len, ))
enc_emb=Embedding(x_voc, embedding_dim, trainable=True)(encoder_inputs)
encoder_lstm1=LSTM(latent_dim, return_sequences=True, return_state=True, dropout=0.4, recurrent_dropout=0.4)
(encoder_output1, state_h1, state_c1)=encoder_lstm1(enc_emb)
encoder_lstm2=LSTM(latent_dim, return_sequences=True, return_state=True, dropout=0.4, recurrent_dropout=0.4)
(encoder_output2, state_h2, state_c2)=encoder_lstm2(encoder_output1)
encoder_lstm3=LSTM(latent_dim, return_state=True, return_sequences=True, dropout=0.4, recurrent_dropout=0.4)
(encoder_outputs, state_h, state_c)=encoder_lstm3(encoder_output2)
decoder_inputs=Input(shape=(None, ))
dec_emb_layer=Embedding(y_voc, embedding_dim, trainable=True)
dec_emb=dec_emb_layer(decoder_inputs)
decoder_lstm=LSTM(latent_dim, return_sequences=True, return_state=True, dropout=0.4, recurrent_dropout=0.2)
(decoder_outputs, decoder_fwd_state, decoder_back_state)=decoder_lstm(dec_emb, initial_state=[state_h, state_c])
decoder_dense=TimeDistributed(Dense(y_voc, activation='softmax'))
decoder_outputs=decoder_dense(decoder_outputs)
model=Model([encoder_inputs, decoder_inputs], decoder_outputs)
model.summary()

#Training
model.compile(optimizer='rmsprop', loss='sparse_categorical_crossentropy')
es=EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=2)
history = model.fit(
    [x_tr, y_tr[:, :-1]],
    y_tr.reshape(y_tr.shape[0], y_tr.shape[1], 1)[:, 1:],
    epochs=1,
    callbacks=[es],
    batch_size=32,
    validation_data=([x_val, y_val[:, :-1]],
                     y_val.reshape(y_val.shape[0], y_val.shape[1], 1)[:, 1:]),
    )

model.save('myModel.h5')