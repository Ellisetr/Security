import random


def primeGen():
    """Метод генерации простого числа"""
    gen = 0
    while primeCheck(gen) is not True:
        gen = random.randint(0, 100000)
    return gen


def primeCheck(n):
    """Проверка числа на то, простое ли оно"""
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
    """Подметод проверки числа на то, простое ли оно"""
    if pow(a, d, n) == 1:
        return False
    for i in range(s):
        if pow(a, 2 ** i * d, n) == n - 1:
            return False
    return True

def genMult(p):
    """Генератор мультипликативной группы"""
    f = p - 1
    n = f
    i = 2
    list_mult = []
    while i * i <= n:
        if n % i == 0:
            list_mult.append(i)
            while n % i == 0:
                n //= i
        i += 1
    if n > 1:
        list_mult.append(n)
    for res in range(2, p + 1):
        check = True
        i = 0
        while i < len(list_mult) and check:
            check = check and pow(res, f // list_mult[i], p) != 1
            i += 1
        if check:
            return res
    return -1

def safePrimeGen():
    """Генератор безопасного простого"""
    N = random.randint(1, 100000)
    while primeCheck(N) is False and primeCheck(int((N-1)/2)) is False:
        N = random.randint(1, 100000)
    print(primeCheck(N))
    return N

