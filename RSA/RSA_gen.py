import math
import random


def primeCheck(n):
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


def generateRandomPrime(left_border, right_border):
    while True:
        number = random.randint(left_border, right_border)
        if primeCheck(number):
            return number


def eulerFunction(p, q):
    return (p - 1) * (q - 1)


def generateOpenExponent(f):
    while True:
        open_exponent = generateRandomPrime(2, f - 1)
        if math.gcd(f, open_exponent) == 1:
            return open_exponent


def calc_prim_root(mod):
    prime_multipliers_set = set(factorize_number(mod - 1))
    for g in range(1, mod):
        for m in prime_multipliers_set:
            if g ** ((mod - 1) / m) % mod == 1:
                break
            return g


def generate_safe_prime(left_border, right_border):
    while True:
        q = generateRandomPrime(left_border, right_border)
        n = 2 * q + 1
        if primeCheck(n):
            return n


def calculate_multiplier(number):
    x = [random.randint(2, 20)]
    while True:
        x.append((x[-1] ** 2 - 1) % number)
        for j in range(len(x) - 1):
            gcd = math.gcd(number, abs(x[-1] - x[j]))
            if gcd != 1:
                return gcd


def factorize_number(number):
    multipliers = []
    buf = number
    while not primeCheck(buf):
        multiplier = calculate_multiplier(buf)
        multipliers.append(multiplier)
        buf = int(buf / multiplier)
    multipliers.append(buf)
    flag = True
    while flag:
        for multiplier in multipliers:
            if not primeCheck(multiplier) and multiplier > 2:
                flag = True
                multipliers.remove(multiplier)
                buf = []
                while not primeCheck(multiplier) and multiplier > 2:
                    tmp_multiplier = calculate_multiplier(multiplier)
                    while tmp_multiplier == multiplier:
                        tmp_multiplier = calculate_multiplier(multiplier)
                    buf.append(tmp_multiplier)
                    multiplier = int(multiplier / tmp_multiplier)
                buf.append(multiplier)
                multipliers += buf
            flag = False
            for m in multipliers:
                if not primeCheck(m) and m > 2:
                    flag = True
    return sorted(multipliers)


def pow_mod(base, index_n, modulus):
    c = 1
    for i in range(1, index_n):
        print(i)
        c = (c * base) % modulus
    return c
