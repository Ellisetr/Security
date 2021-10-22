import SHA_const


def str_to_bin(string):
    output = ''
    for symbol in string:
        output += bin(ord(symbol))[2:].zfill(8)
    return output


def fill_length(input_string, input_length):
    binary_length = bin(input_length)[2:].zfill(64)
    return input_string + binary_length


def format_input(input_string):
    input_string = str_to_bin(input_string)
    input_length = len(input_string)
    input_string += '1'
    while len(input_string) % 512 != 448:
        input_string += '0'
    return fill_length(input_string, input_length)


def create_message_schedule(message):
    message_schedule = []
    for i in range(0, len(message), 32):
        message_schedule.append(message[i:i + 32])
    for i in range(48):
        word = ''
        for j in range(32):
            word += '0'
        message_schedule.append(word)
    return message_schedule


def change_indexes(message):
    for i in range(16, 64):
        temp_1 = message[i - 15][-7:] + message[i - 15][:-7]
        temp_2 = message[i - 15][-18:] + message[i - 15][:-18]
        temp_3 = '000' + message[i - 15][:-3]
        string_0 = bin(int(temp_1, 2) ^ int(temp_2, 2) ^ int(temp_3, 2))[2:]

        temp_1 = message[i - 2][-17:] + message[i - 2][:-17]
        temp_2 = message[i - 2][-19:] + message[i - 2][:-19]
        temp_3 = '0' * 10 + message[i - 2][:-10]
        string_1 = bin(int(temp_1, 2) ^ int(temp_2, 2) ^ int(temp_3, 2))[2:]

        result = (int(message[i - 16], 2) + int(string_0, 2) + int(message[i - 7], 2) + int(string_1, 2)) % 2 ** 32

        message[i] = bin(result)[2:].zfill(32)
    return message


def compress(words):
    a = bin(SHA_const.h0)[2:].zfill(32)
    b = bin(SHA_const.h1)[2:].zfill(32)
    c = bin(SHA_const.h2)[2:].zfill(32)
    d = bin(SHA_const.h3)[2:].zfill(32)
    e = bin(SHA_const.h4)[2:].zfill(32)
    f = bin(SHA_const.h5)[2:].zfill(32)
    g = bin(SHA_const.h6)[2:].zfill(32)
    h = bin(SHA_const.h7)[2:].zfill(32)

    for i in range(64):
        temp_1 = e[-6:] + e[:-6]
        temp_2 = e[-11:] + e[:-11]
        temp_3 = e[-25:] + e[:-25]
        string_1 = bin(int(temp_1, 2) ^ int(temp_2, 2) ^ int(temp_3, 2))[2:]
        char = bin((int(e, 2) & int(f, 2)) ^ (~int(e, 2) & int(g, 2)))[2:]
        buff_1 = (int(h, 2) + int(string_1, 2) + int(char, 2) + SHA_const.k[i] + int(words[i], 2)) % 2 ** 32

        temp_1 = a[-2:] + a[:-2]
        temp_2 = a[-13:] + a[:-13]
        temp_3 = a[-22:] + a[:-22]
        string_0 = bin(int(temp_1, 2) ^ int(temp_2, 2) ^ int(temp_3, 2))[2:]
        maj = bin((int(a, 2) & int(b, 2)) ^ (int(a, 2) & int(c, 2)) ^ (int(b, 2) & int(c, 2)))[2:]
        buff_2 = (int(string_0, 2) + int(maj, 2)) % 2 ** 32

        h = g
        g = f
        f = e
        e = bin((int(d, 2) + buff_1) % 2 ** 32)[2:].zfill(32)
        d = c
        c = b
        b = a
        a = bin((buff_1 + buff_2) % 2 ** 32)[2:].zfill(32)

    h0 = hex((SHA_const.h0 + int(a, 2)) % 2 ** 32)[2:]
    h1 = hex((SHA_const.h1 + int(b, 2)) % 2 ** 32)[2:]
    h2 = hex((SHA_const.h2 + int(c, 2)) % 2 ** 32)[2:]
    h3 = hex((SHA_const.h3 + int(d, 2)) % 2 ** 32)[2:]
    h4 = hex((SHA_const.h4 + int(e, 2)) % 2 ** 32)[2:]
    h5 = hex((SHA_const.h5 + int(f, 2)) % 2 ** 32)[2:]
    h6 = hex((SHA_const.h6 + int(g, 2)) % 2 ** 32)[2:]
    h7 = hex((SHA_const.h7 + int(h, 2)) % 2 ** 32)[2:]

    return h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7


def encrypt_sha(message):
    return compress(change_indexes(create_message_schedule(format_input(message))))
