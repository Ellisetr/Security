import RSA_gen
import Reciever
import Sender


def Start():
    receiver = Reciever.Receiver(RSA_gen.generateRandomPrime(1000, 2000), RSA_gen.generateRandomPrime(1000, 2000))
    sender = Sender.Sender(receiver.public_key)
    message = sender.encryptMessage('Hello MIREA')
    print('Encrypted string:', message)
    print('Decrypted message:', receiver.decryptMessage(message), '\n')
