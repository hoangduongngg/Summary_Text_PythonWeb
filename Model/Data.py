class Data:
    def __init__(self, content, summary, istrained):
        self.id = None
        self.content = content
        self.summary = summary
        self.istrained = istrained
    # Dương: sửa hàm init, chỉ cần khởi tạo 3 giá trị
    def __init__(self, content, summary, istrained):
        self.content = content
        self.summary = summary
        self.istrained = istrained

    def __str__(self):
        return str(self.id) + ' ' + str(self.content) + ' ' + str(self.summary) + ' ' + str(self.istrained)
