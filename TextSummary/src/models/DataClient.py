class DataClient:
    def __init__(self):
        self._content=None
        self._sum=None
    def setContent(self, content):
        self._content=content
    def setSum(self, sum):
        self._sum=sum

    def getContent(self):
        return self._content
    def getSum(self):
        return self._sum
