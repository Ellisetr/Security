import collections
import copy


class Encrypt:
    def __init__(self, shift, keyword, text, alphabet):
        self.alphabet = alphabet
        self.keyword = list(self.checkKeyword(keyword.upper()))
        self.alphabetDict = dict(zip(copy.copy(self.alphabet), self.caesarAlphabet(shift, copy.copy(self.alphabet))))
        self.encryptedText = self.encrypt(open(text).read())

    def checkKeyword(self, keyword):
        if len(list(set(keyword))) == len(keyword):
            for letterWord in keyword:
                if letterWord not in self.alphabet:
                    raise Exception
            else:
                return keyword
        else:
            raise Exception

    def caesarAlphabet(self, shift, input_alphabet):
        for letterKeyword in self.keyword:
            for letter in input_alphabet:
                if letterKeyword == letter:
                    input_alphabet.remove(letter)
        input_alphabet = collections.deque(input_alphabet)
        input_alphabet.extendleft(reversed(self.keyword))
        input_alphabet.rotate(shift)
        return input_alphabet

    def encrypt(self, input_text):
        output_text = ""
        for input_letter in input_text:
            if input_letter.upper() in self.alphabetDict:
                if input_letter.isupper():
                    output_text += self.alphabetDict.get(input_letter.upper())
                else:
                    output_text += (self.alphabetDict.get(input_letter.upper())).lower()
            else:
                output_text += input_letter
        return output_text
