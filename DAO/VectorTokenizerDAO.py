from DAO.DAO import DAO
from Model.VectorTokenizer import VectorTokenizer
import pickle
import os

class VectorTokenizerDAO(DAO):
    def __init__(self):
        super().__init__()
    
    def getTrainTokenizer(self, id):
        #statement
        cursor=self.con.cursor()
        sql="SELECT * FROM tblTokenizer WHERE id=%s"
        cursor.execute(sql, [id])
        result=cursor.fetchall()
        vectorTokenizer=VectorTokenizer()
        tokenizer=pickle.load(open(os.getcwd()+'\TextSummary'+result[0][1], 'rb'))
        vectorTokenizer.setAttr(id, tokenizer, url=result[0][1])
        return vectorTokenizer



        
