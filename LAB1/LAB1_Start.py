from main import RUSSIAN_ALPHABET_FREQUENCY, RUSSIAN_ALPHABET
from LAB1 import LAB1_Decrypt
from LAB1 import LAB1_Encrypt

def Start():
    Encrypt = LAB1_Encrypt.Encrypt(5, 'ключ', 'LAB1/input_text.txt', RUSSIAN_ALPHABET)
    print("Encrypted alphabet:")
    print(Encrypt.alphabetDict)
    print("\n" + "Encrypted text:")
    print(Encrypt.encryptedText + "\n")
    Decrypt = LAB1_Decrypt.Decrypt(Encrypt.encryptedText, RUSSIAN_ALPHABET_FREQUENCY, RUSSIAN_ALPHABET)
    print("Decrypted monogram text:")
    print(Decrypt.output_monogram_decr + "\n")
    print("Decrypted bigram text:")
    print(Decrypt.output_bigram_decr)



