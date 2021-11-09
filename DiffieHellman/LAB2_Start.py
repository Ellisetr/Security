from DiffieHellman import MITE, MITM
from CustomClasses import CustomMath


def Start():
    g = CustomMath.primeGen()
    p = CustomMath.primeGen()

    Alice = MITE.ManInTheEnd(g, p, CustomMath.primeGen(), "Alice")
    Bob = MITE.ManInTheEnd(g, p, CustomMath.primeGen(), "Bob")
    Eve = MITM.ManInTheMiddle(g, p, "Eve")

    key = Alice.generate_partial_key()
    Bob.generate_full_key(key)
    Eve.catchKey(key)

    key = Bob.generate_partial_key()
    Alice.generate_full_key(key)
    Eve.catchKey(key)

    Eve.hack()

    msg = Bob.encrypt_message("Hello world")
    Eve.catchMessage(msg)
    Alice.decrypt_message(msg)

    msg = Alice.encrypt_message("How are you?")
    Eve.catchMessage(msg)
    Bob.decrypt_message(msg)

