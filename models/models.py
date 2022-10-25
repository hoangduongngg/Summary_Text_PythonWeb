from ast import main
from app import db
from sqlalchemy import Column, Integer, String, Boolean

class Data(db.Model):
    
    id = Column(db.Integer, primary_key = True, autoincrement = True)
    content = Column(String(5000))
    summary = Column(String(500))
    isTrained = Column(Boolean) 

    def __init__(self, content, summary, isTrained):
        self.content = content
        self.summary = summary
        self.isTrained = isTrained

if __name__ == "__main__":
    db.create_all()