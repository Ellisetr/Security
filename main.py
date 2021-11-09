from CustomClasses import CustomHash
from LAB1 import LAB1_Start
from DiffieHellman import LAB2_Start
from RSA import RSA_LAB
from SRP2 import SRP_LAB

if __name__ == '__main__':
    print("Caesar chipper:")
    LAB1_Start.Start()
    print("Diffie-Hellman + Rabin-Miller number generator:")
    LAB2_Start.Start()
    print("RSA:")
    RSA_LAB.Start()
    print("Hash func:")
    print(hex(CustomHash.hash_func("Helloworld")),"\n")
    print("SRP:")
    SRP_LAB.Start()
