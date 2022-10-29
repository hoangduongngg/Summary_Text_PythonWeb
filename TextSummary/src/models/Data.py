from src.models.DataClient import DataClient

class Data(DataClient):
    def __init(self):
        super().__init__()
        self.__id=None
        self.__isTrained=None
    
    def setAttr(self, id, content, sum, isTrained):
        self.__id=id
        self._content=content
        self._sum=sum
        self.__isTrained=isTrained
    
    def getId(self):
        return self.__id
