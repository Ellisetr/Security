import random


def primeGen():
    gen = 0
    while primeCheck(gen) is not True:
        gen = random.randint(0, 100000)
    return gen


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


def SafePrimeGen():
    N = 0
    while primeCheck(N) is not True and primeCheck(int((N-1)/2)) is not True:
        N = random.randint(1, 100000)
    return N
