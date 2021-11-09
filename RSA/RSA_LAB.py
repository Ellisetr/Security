import math
import random


class Encrypt():
    def __init__(self, public_key):
        self.public_key = public_key

    def encr(self, message):
        return [ord(character) ** self.public_key[0] % self.public_key[1] for character in message]


class Decrypt:
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.n = self.p * self.q
        self.euler = (self.p - 1) * (self.q - 1)
        self.e = based_num_gen(self.euler)
        self.d = extended_equlid(self.e, self.euler)
        self.public_key = [self.e, self.n]
        self.secret_key = [self.d, self.n]
        print(self.public_key)
        print(self.secret_key)

    def get_pub_key(self):
        return self.public_key

    def get_sec_key(self):
        return self.secret_key

    def decr(self, text):
        return "".join(chr(char ** self.secret_key[0] % self.secret_key[1]) for char in text)


def extended_equlid(e, euler):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_euler = euler

    while e > 0:
        temp1 = temp_euler // e
        temp2 = temp_euler - temp1 * e
        temp_euler = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y
    if temp_euler == 1:
        return d + euler


def based_num_gen(f):
    open_exp = genPrime(2, f - 1)
    if math.gcd(f, open_exp) == 1:
        return open_exp


def genPrime(left, right):
    while True:
        number = random.randint(left, right)
        if checkPrime(number):
            return number


def checkPrime(n):
    if n % 2 == 0:
        return False
    s = 0
    d = n - 1
    while n % 2 == 0:
        d >>= 2
        s += 1
    for i in range(5):
        a = random.randrange(2, n)
        if check(a, d, n, s):
            return False
    return True


def check(a, d, n, s):
    if pow(a, d, n) == 1:
        return False
    for i in range(s):
        if pow(a, 2 ** i * d, n) == n - 1:
            return False
    return True


def Start():
    decr = Decrypt(genPrime(500, 1000), genPrime(500, 1000))
    encr = Encrypt(decr.get_pub_key())
    text = encr.encr("hello world")
    print(text)
    print(decr.decr(text))

