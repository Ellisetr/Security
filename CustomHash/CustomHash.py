""""
Первоначальная версия, показанная, сделанная и сданная на паре 23.10.21
def hash_func(text):
    byte_len = 0
    output = ''
    hash_list = []
    length = len(text)
    for letter in text:
        byte_len += ord(letter)
        hash_list.append(ord(letter) ** length)
    list_buff = []
    for item in hash_list:
        list_buff.append(item % byte_len)
    list_buff1 = []
    for item in list_buff:
        buff = bin(item)[2:]
        if len(buff) < 32:
            buff = buff.zfill(32 - len(buff))
        elif len(buff) > 32:
            buff = buff[(32 - len(buff)):]
        buff = int(buff, 2) ^ int(length) ^ int(byte_len)
        list_buff1.append(hex(buff)[2:])
    for item in list_buff1:
        output += item
    return output

"""


# Оптимизированная версия:
def hash_func(text):
    # Счётчик суммы кодов символов
    byte_len = 0
    # Выходная строка
    output = ''
    # Длинна входной строки
    length = len(text)
    # Сложение ASCII кодов символов
    for letter in text:
        byte_len += ord(letter)
    # Хэширование, используя возведения каждого символа
    # в степень длинны строки и модуля по сумме кодов символов
    # с последующим XORом с длинной строки и суммой кодов
    for letter in text:
        buff = bin(ord(letter) ** length % byte_len)[2:]
        # Приведение к 32 битам
        if len(buff) < 32:
            buff = buff.zfill(32 - len(buff))
        elif len(buff) > 32:
            buff = buff[(32 - len(buff)):]
        # XOR над символами
        buff = int(buff, 2) ^ int(length) ^ int(byte_len)
        # Формирование выходной строки
        output += hex(buff)[2:]
    return output

