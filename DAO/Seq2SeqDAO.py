from DAO.VectorTokenizerDAO import VectorTokenizerDAO
from DAO.DAO import DAO
from Model.Seq2Seq import Seq2Seq
import tensorflow as tf
import os
from Model.attention import AttentionLayer
from datetime import datetime
import pickle

class Seq2SeqDAO(DAO):
    def __init__(self):
        super().__init__()
    
    def getModelPreTrain(self):
        #statement
        cursor=self.con.cursor()
        sql="SELECT * FROM tblSeq2Seq WHERE active=1"
        cursor.execute(sql)
        result=cursor.fetchall()
        model=tf.keras.models.load_model(os.getcwd()+'\TextSummary'+result[0][2], custom_objects={'AttentionLayer': AttentionLayer})
        vecDAO=VectorTokenizerDAO()
        xTokenizer=vecDAO.getTrainTokenizer(result[0][10])
        yTokenizer=vecDAO.getTrainTokenizer(result[0][11])
        seq2Seq=Seq2Seq(result[0][6], result[0][7], result[0][8], result[0][9], xTokenizer, yTokenizer)
        seq2Seq.setModel(model)
        seq2Seq.setAttrDB(result[0][0], result[0][1], result[0][2], result[0][5], result[0][3], result[0][4])
        return seq2Seq
    
    def saveModel(self, seq2Seq):
        cursor=self.con.cursor()
        sql="SELECT MAX(VERSION) FROM tblSeq2Seq"
        cursor.execute(sql)
        result=cursor.fetchall()
        now=datetime.now()
        dateNow=str(now.strftime("%Y-%m-%d"))
        timeNow=str(now.strftime("%H%M%S"))
        urlModel=r"\src\static\model\modelTemp"+str(result[0][0]+1)+r".h5"
        urlXTokenizer=r"\src\static\data-pre\x_tokenizer"+dateNow+timeNow+r".pkl"
        urlYTokenizer=r"\src\static\data-pre\y_tokenizer"+dateNow+timeNow+r".pkl"
        seq2Seq.getModel().save(os.getcwd()+'\TextSummary'+urlModel)
        pickle.dump(seq2Seq.getXTokenizer().getVectorModel(), open(os.getcwd()+'\TextSummary'+urlXTokenizer, 'wb'))
        pickle.dump(seq2Seq.getYTokenizer().getVectorModel(), open(os.getcwd()+'\TextSummary'+urlYTokenizer, 'wb'))
        sql="INSERT INTO tblTokenizer (url) VALUES (%s)"
        cursor.execute(sql, [urlXTokenizer])
        idXTokenizer=cursor.lastrowid
        cursor.execute(sql, [urlYTokenizer])
        idYTokenizer=cursor.lastrowid
        sql="INSERT INTO tblseq2seq (version, url, createAt, active, maxTextLen, maxSummaryLen, embeddingDim, latentDim, idXTokenizer, idYTokenizer) "
        sql+="VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, [result[0][0]+1, urlModel, dateNow, 0, seq2Seq.getMaxTextLen(), \
            seq2Seq.getMaxSummaryLen(), seq2Seq.getEmbeddingDim(), seq2Seq.getLatentDim(), \
            str(idXTokenizer), str(idYTokenizer)])
        self.con.commit()
        #self.con.rollback()

    