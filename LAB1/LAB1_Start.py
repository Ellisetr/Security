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
    print(Decrypt.output_bigram_decr+"\n")


RUSSIAN_ALPHABET = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т',
                    'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
RUSSIAN_ALPHABET_FREQUENCY1 = {'о': 0.09, 'е': 0.072, 'а': 0.062, 'и': 0.062, 'н': 0.055,
                               'т': 0.053, 'с': 0.045, 'р': 0.04, 'в': 0.038, 'л': 0.035, 'к': 0.028, 'м': 0.026,
                               'д': 0.025, 'п': 0.023, 'у': 0.021, 'я': 0.018, 'ы': 0.016, 'з': 0.016, 'ь': 0.014,
                               'ъ': 0.014, 'б': 0.014, 'г': 0.013, 'ч': 0.012, 'й': 0.010, 'х': 0.009, 'ж': 0.007,
                               'ю': 0.006, 'ш': 0.006, 'ц': 0.004, 'щ': 0.003, 'э': 0.003, 'ф': 0.002}
RUSSIAN_ALPHABET_FREQUENCY = {'о': 0.01097, 'а': 0.00845, 'е': 0.00801, 'н': 0.00735, 'и': 0.0067, 'т': 0.00626,
                              'л': 0.00547, 'с': 0.00473, 'в': 0.00454, 'р': 0.0044, 'у': 0.00349, 'к': 0.00321,
                              'д': 0.00298, 'п': 0.00281, 'м': 0.00262, 'б': 0.00201, 'я': 0.0019, 'ь': 0.00174,
                              'г': 0.0017, 'з': 0.00165, 'ы': 0.00159, 'щ': 0.00144, 'й': 0.00121, 'х': 0.00097,
                              'э': 0.00094, 'ш': 0.00073, 'ю': 0.00064, 'ц': 0.00048, 'ч': 0.00036, 'ж': 0.00032,
                              'ф': 0.00026, 'ъ': 0.00004}