import tensorflow as tf
from keras.layers import Input, LSTM, Embedding, Dense, TimeDistributed, Concatenate
from Model.attention import AttentionLayer
from keras.models import Model
import numpy as np

class Seq2Seq:
    def __init__(self, maxTextLen, maxSummaryLen, embeddingDim, latentDim, xTokenizer, yTokenizer):
        self.__maxTextLen=maxTextLen
        self.__maxSummaryLen=maxSummaryLen
        self.__embeddingDim=embeddingDim
        self.__latentDim=latentDim
        self.__xTokenizer=xTokenizer
        self.__yTokenizer=yTokenizer
        x_voc=self.__xTokenizer.getVectorModel().num_words
        y_voc=self.__yTokenizer.getVectorModel().num_words
        with tf.device('/cpu:0'):
            encoder_inputs=Input(shape=(self.__maxTextLen,))
            enc_emb=Embedding(x_voc, self.__embeddingDim, trainable=True)(encoder_inputs)
            encoder_lstm1=LSTM(self.__latentDim, return_sequences=True, return_state=True, dropout=0.4, recurrent_dropout=0.4)
            encoder_output1, state_h1, state_c1=encoder_lstm1(enc_emb)
            encoder_lstm2=LSTM(self.__latentDim, return_sequences=True, return_state=True, dropout=0.4, recurrent_dropout=0.4)
            encoder_output2, state_h2, state_c2=encoder_lstm2(encoder_output1)
            encoder_lstm3=LSTM(self.__latentDim, return_state=True, return_sequences=True, dropout=0.4, recurrent_dropout=0.4)
            encoder_outputs, state_h, state_c=encoder_lstm3(encoder_output2)
            decoder_inputs=Input(shape=(None,))
            dec_emb_layer=Embedding(y_voc, self.__embeddingDim, trainable=True)
            dec_emb=dec_emb_layer(decoder_inputs)
            decoder_lstm=LSTM(self.__latentDim, return_sequences=True, return_state=True, dropout=0.4, recurrent_dropout=0.2)
            decoder_outputs, decoder_fwd_state, decoder_back_state=decoder_lstm(dec_emb, initial_state=[state_h, state_c])
            attn_layer=AttentionLayer(name='attention_layer')
            attn_out, attn_states=attn_layer([encoder_outputs, decoder_outputs])
            decoder_concat_input=Concatenate(axis=-1, name='concat_layer')([decoder_outputs, attn_out])
            decoder_dense=TimeDistributed(Dense(y_voc, activation='softmax'))
            decoder_outputs=decoder_dense(decoder_concat_input)
            self.__model=Model([encoder_inputs, decoder_inputs], decoder_outputs)
            self.__model.compile(optimizer='rmsprop', loss='sparse_categorical_crossentropy')
            self.__encoderModel=Model(inputs=encoder_inputs, outputs=[encoder_outputs, state_h, state_c])
            decoder_state_input_h=Input(shape=(self.__latentDim, ))
            decoder_state_input_c=Input(shape=(self.__latentDim, ))
            decoder_hidden_state_input=Input(shape=(self.__maxTextLen, self.__latentDim))
            dec_emb2=dec_emb_layer(decoder_inputs)
            (decoder_outputs2, state_h2, state_c2)=decoder_lstm(dec_emb2, initial_state=[decoder_state_input_h, decoder_state_input_c])
            attn_out_inf, attn_states_inf=attn_layer([decoder_hidden_state_input, decoder_outputs2])
            decoder_inf_concat=Concatenate(axis=-1, name='concat')([decoder_outputs2, attn_out_inf])
            decoder_outputs2=decoder_dense(decoder_inf_concat)
            self.__decoderModel=Model([decoder_inputs]+[decoder_hidden_state_input,
                                decoder_state_input_h, decoder_state_input_c],
                                [decoder_outputs2] + [state_h2, state_c2])

    def setModel(self, model):
        self.__model.set_weights(model.get_weights())

    def summary(self):
        self.__model.summary()

    def getModel(self):
        return self.__model

    def decode_sequence(self, input_seq):
        reverse_target_word_index=self.__yTokenizer.getVectorModel().index_word
        target_word_index=self.__yTokenizer.getVectorModel().word_index
        with tf.device('/cpu:0'):
            (e_out, e_h, e_c)=self.__encoderModel.predict(input_seq)
            target_seq=np.zeros((1, 1))
            target_seq[0, 0]=target_word_index['sostok']
            stop_condition=False
            decoded_sentence=''
            while not stop_condition:
                (output_tokens, h, c)=self.__decoderModel.predict([target_seq]+[e_out, e_h, e_c])
                sampled_token_index=np.argmax(output_tokens[0, -1, :])
                sampled_token=reverse_target_word_index[sampled_token_index]
                if sampled_token!='eostok':
                    decoded_sentence+=' '+sampled_token

                if sampled_token=='eostok' or len(decoded_sentence.split())>=self.__maxSummaryLen-1:
                    stop_condition=True

                target_seq=np.zeros((1, 1))
                target_seq[0, 0]=sampled_token_index

                (e_h, e_c)=(h, c)
            return decoded_sentence

    def seq2summary(self, input_seq):
        newString=''
        target_word_index=self.__yTokenizer.getVectorModel().word_index
        reverse_target_word_index=self.__yTokenizer.getVectorModel().index_word
        for i in input_seq:
            if i!=0 and i!=target_word_index['sostok'] and i!=target_word_index['eostok']:
                newString=newString+reverse_target_word_index[i]+' '
        return newString

    def seq2text(self, input_seq):
        newString=''
        reverse_source_word_index=self.__xTokenizer.getVectorModel().index_word
        for i in input_seq:
            if i!=0:
                newString=newString+reverse_source_word_index[i]+' '
        return newString

    def predrict(self, x):
        with tf.device('/cpu:0'):
            print('Review:', self.seq2text(x))
            summary=self.decode_sequence(x.reshape(1, self.__maxTextLen))
            print('Predicted summary:', summary)
            return summary
            
    def fit(self, x_tr, y_tr, x_val=None, y_val=None):
        with tf.device('/cpu:0'):
            callback=tf.keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=2)
            history=self.__model.fit(
                [x_tr, y_tr[:, :-1]],
                y_tr.reshape(y_tr.shape[0], y_tr.shape[1], 1)[:, 1:],
                epochs=1,
                callbacks=[callback],
                batch_size=2,
                #validation_data=([x_val,y_val[:, :-1]], y_val.reshape(y_val.shape[0], y_val.shape[1], 1)[:, 1:]),
            )

    def setAttrDB(self, id, version, url, active, f1Score=None, createAt=None):
        self.__id=id
        self.__version=version
        self.__url=url
        self.__f1Score=f1Score
        self.__createAt=createAt
        self.__active=active

    def getXTokenizer(self):
        return self.__xTokenizer
        
    def getYTokenizer(self):
        return self.__yTokenizer

    def getMaxTextLen(self):
        return self.__maxTextLen
    
    def getMaxSummaryLen(self):
        return self.__maxSummaryLen
    
    def getEmbeddingDim(self):
        return self.__embeddingDim
    
    def getLatentDim(self):
        return self.__latentDim
    