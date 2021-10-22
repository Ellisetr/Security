class Sender:
    def __init__(self, public_key):
        self.receiver_public_key = public_key

    def encryptMessage(self, text):
        output = []
        for character in text:
            output.append(ord(character) ** self.receiver_public_key[0] % self.receiver_public_key[1])
        return output
