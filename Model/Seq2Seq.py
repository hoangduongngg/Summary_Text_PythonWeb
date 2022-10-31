class Seq2Seq:
    def __init__(self, model, version, url, f1Score, createAt, active):
        self.model = model
        self.version = version
        self.url = url
        self.f1Score = f1Score
        self.createAt = createAt
        self.active = active


    def __str__(self):
        return str(self.model) + ' ' + str(self.version) + ' ' + str(self.url) + ' ' + str(self.f1Score) + ' ' + str(self.createAt) + ' ' + str(self.active)
