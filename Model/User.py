class User:
    def __init__(self, username, password):
        self.is_authenticated = None
        self.username = username
        self.password = password

    def __str__(self):
        return str(self.username) + ' ' + str(self.password)
