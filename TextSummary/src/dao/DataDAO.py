from src.dao.DAO import DAO
from src.models.Data import Data
import pandas as pd

class DataDAO(DAO):
    def __init__(self):
        super().__init__()
    
    def getPercentageSampleNew(self):
        cursor=self.con.cursor()
        sql="SELECT * FROM tblData WHERE isTrained=%s"
        cursor.execute(sql, [1])
        resultTrain=cursor.fetchall()
        countSampleTrain=len(resultTrain)
        cursor.execute(sql, [0])
        resultNoTrain=cursor.fetchall()
        countSampleNoTrain=len(resultNoTrain)
        listSampleNoTrain=[]
        listSampleTrained=[]
        for i in range(len(resultNoTrain)):
            data=Data()
            data.setAttr(resultNoTrain[i][0], resultNoTrain[i][1], resultNoTrain[i][2], resultNoTrain[i][3])
            listSampleNoTrain.append(data)
        for i in range(len(resultTrain)):
            data=Data()
            data.setAttr(resultTrain[i][0], resultTrain[i][1], resultTrain[i][2], resultTrain[i][3])
            listSampleTrained.append(data)

        return ((countSampleNoTrain+0.001)/(countSampleTrain+0.001), listSampleTrained, listSampleNoTrain)
    
    def updateSampleNoTrain(self, list):
        cursor=self.con.cursor()
        try:
            for i in range(len(list)):
                sql="UPDATE tblData SET isTrained='1' WHERE id=%s"
                cursor.execute(sql, [list[i].getId()])
            self.con.commit()
        except:
            self.con.rollback()