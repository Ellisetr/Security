class ManInTheMiddle:
    def __init__(self, g, p, name):
        self.g = g
        self.p = p
        self.name = name
        self.keys = []

    def hack(self):
        None

    def catchMessage(self, message):
        print(self.name, "caught message", message)

    def catchKey(self, key):
        self.keys.append(key)
        print(self.name, "caught key", key,"\n")
