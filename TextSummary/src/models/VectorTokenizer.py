from keras.preprocessing.text import Tokenizer

class VectorTokenizer:
    def __init__(self):
        self.__id=None
        self.__tokenizer=Tokenizer()
        self.__url=None
    
    def setAttr(self, id, tokenizer, url):
        self.__id=id
        self.__tokenizer=tokenizer
        self.__url=url

    def createTokenizer(self, x, numWords):
        self.__tokenizer=Tokenizer(num_words=numWords+1)
        self.__tokenizer.fit_on_texts(list(x))

    def getId(self):
        return self.__id

    def getVectorModel(self):
        return self.__tokenizer

    def getUrl(self):
        return self.__url