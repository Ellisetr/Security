import CustomHash
from LAB1 import LAB1_Start
from DiffieHellman import LAB2_Start
from RSA import RSA_LAB
from SRP2 import SRP_LAB

if __name__ == '__main__':
    print("Caesar chipper:")
    LAB1_Start.Start()
    print("Diffie-Hellman + Rabin-Miller number generator:")
    LAB2_Start.Start()
    print("Hash func:")
    print(CustomHash.hash_func("Helloworld"))
    print("SRP:")
    SRP_LAB.Start()
