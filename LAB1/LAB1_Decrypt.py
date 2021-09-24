import copy


class Decrypt:
    def __init__(self, input_text, input_frequency, input_alphabet):
        self.input_text = input_text
        self.input_frequency = input_frequency
        self.input_alphabet = input_alphabet
        self.letter_counter = 0

        # self.input_text2 = open("input_text2.txt").read()

        # Тест с частотой на основе другого текста
        # self.monogram = self.monogramCounter(self.input_text)
        # self.frequency = self.monogramCounter(self.input_text2)
        # print(self.frequency)
        # self.input_text = self.monogramDecrypt(self.frequency, self.monogram, self.input_text)
        # Прогонка с частотой из интернета

        self.monogram = self.monogramCounter(self.input_text)
        self.monogram_alphabet = self.generateAlphabet(self.input_frequency, self.monogram)
        self.output_monogram_decr = self.monogramDecrypt(self.input_frequency, self.monogram, self.input_text)

        self.bigram = self.bigramCounter(self.input_text)
        self.bigram_frequency = self.bigramCounter(open("LAB1/input_text.txt").read())
        self.output_bigram_decr = self.bigramDecrypt(self.bigram_frequency, self.bigram, self.input_text)

    def monogramCounter(self, input_text):
        output_monogram = dict.fromkeys(self.input_alphabet, 0)
        for letter in input_text:
            if letter.upper() in self.input_alphabet:
                output_monogram[letter.upper()] = output_monogram.get(letter.upper()) + 1
                self.letter_counter = self.letter_counter + 1
        for letter in output_monogram:
            output_monogram[letter] = round(output_monogram.get(letter) / self.letter_counter, 15)
        return output_monogram

    def bigramCounter(self, input_text):
        output_bigram = {}
        for i in range(len(input_text) - 1):
            if input_text[i].upper() in self.input_alphabet and input_text[i+1].upper() in self.input_alphabet:
                if input_text[i].upper() + input_text[i + 1].upper() in output_bigram:
                    output_bigram[input_text[i].upper() + input_text[i + 1].upper()] += 1
                else:
                    output_bigram[input_text[i].upper() + input_text[i + 1].upper()] = 1
        return output_bigram

    def generateAlphabet(self, input_frequency, monogram):
        freq_dict = sorted(input_frequency.items(), key=lambda x: x[1])
        freq_dict2 = sorted(monogram.items(), key=lambda x: x[1])
        output_alphabet = dict(zip([i[0] for i in freq_dict2], [j[0].upper() for j in freq_dict]))
        return output_alphabet

    def monogramDecrypt(self, input_frequency, monogram, input_text):
        freq_dict = sorted(input_frequency.items(), key=lambda x: x[1])
        freq_dict2 = sorted(monogram.items(), key=lambda x: x[1])
        output_alphabet = dict(zip([i[0] for i in freq_dict2], [j[0] for j in freq_dict]))
        output_text = ""
        for input_letter in input_text:
            if input_letter.upper() in output_alphabet:
                if input_letter.isupper():
                    output_text += output_alphabet.get(input_letter.upper()).upper()
                else:
                    output_text += (output_alphabet.get(input_letter.upper())).lower()
            else:
                output_text += input_letter
        return output_text

    def bigramDecrypt(self, input_frequency, bigram, input_text):
        bigram_input = {}
        """
        Maps = copy.copy(open("input_text1.txt").read())
        Lines = Maps.splitlines()
        Result = []
        for line in Lines:
            line = line.split("\t")
            Result = Result + [line]
        for i in range(len(Result)):
            for j in range(len(Result)):
                if Result[i][j] != '-':
                    bigram_input[self.input_alphabet[i] + self.input_alphabet[j]] = Result[i][j]
        
        print(bigram_input)
        freq_dict = sorted(bigram_input.items(), key=lambda x: x[1])
        freq_dict2 = sorted(self.bigramCounter().items(), key=lambda x: x[1])
        output_alphabet = dict(zip([i[0] for i in freq_dict2], [j[0] for j in freq_dict]))
        output_text = ""
                for i in range(len(self.input_text) - 2):
            if self.input_text[i].upper() + self.input_text[i + 1].upper() in output_alphabet:
                output_text += output_alphabet.get(self.input_text[i].upper() + self.input_text[i + 1].upper())
            else:
                output_text += self.input_text[i]
        self.input_text = output_text
        """
        freq_dict = sorted(input_frequency.items(), key=lambda x: x[1])
        freq_dict2 = sorted(bigram.items(), key=lambda x: x[1])
        output_alphabet = dict(zip([i[0] for i in freq_dict2], [j[0] for j in freq_dict]))
        output_text = ""
        i = 0
        for j in range(len(input_text) - 1):
            if i > len(input_text) - 2:
                break
            if input_text[i].upper() + input_text[i + 1].upper() in output_alphabet:
                if input_text[i].isupper():
                    if input_text[i + 1].isupper():
                        output_text += output_alphabet.get(input_text[i] + input_text[i + 1])
                    else:
                        output_text += output_alphabet.get(input_text[i] + input_text[i + 1].upper())[0] + \
                                       output_alphabet.get(input_text[i] + input_text[i + 1].upper())[1].lower()
                else:
                    if input_text[i + 1].isupper():
                        output_text += output_alphabet.get(input_text[i].upper() + input_text[i + 1])[0].lower() + \
                                       output_alphabet.get(input_text[i].upper() + input_text[i + 1])[1]
                    else:
                        output_text += output_alphabet.get(input_text[i].upper() + input_text[i + 1].upper()).lower()
                i += 2
            else:
                if input_text[i].islower() and input_text[i].upper() in self.monogram_alphabet:
                    output_text += self.monogram_alphabet.get(input_text[i].upper()).lower()
                elif input_text[i].isupper() and input_text[i] in self.monogram_alphabet:
                    output_text += self.monogram_alphabet.get(input_text[i]).upper()
                else:
                    output_text += input_text[i]
                i += 1
        return output_text

    def test(self):
        return None
