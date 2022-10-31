from DAO import DAO1
from Model.Seq2Seq import Seq2Seq

conn = DAO1.connectDB()
cursor = conn.cursor()

def getSeq2SeqList():
    seq2SeqList = []
    cursor.execute('SELECT * FROM tblseq2seq')
    for row in cursor.fetchall():
        seq2SeqList.append({"id": row[0],"version": row[1], "url": row[2], "f1Score": row[3], "createAt": row[4], "active": row[5]})
    return seq2SeqList

def setActiveModelSeq2Seq(version):
    cursor.execute('UPDATE tblseq2seq SET active = 0 WHERE active = 1')
    cursor.execute('UPDATE tblseq2seq SET active = 1 WHERE version = {0}'.format(version))
    conn.commit()