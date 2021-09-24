import random

def rabinovich(n):
    if n % 2 == 0:
        raise Exception('Number is even!')
    s = 0
    d = n - 1

    while n % 2 == 0:
        d >>= 2
        s += 1
    print(f'd is {d}, s is {s}')

    for i in range(5):
        a = random.randrange(2, n)
        if check(a, d, n, s):
            return False
    return True

def check(a, d, n, s):
    if pow(a, d ,n) == 1:
        return False
    for i in range(s):
        if pow(a, 2**i * d, n) == n - 1:
            return False
    return True

print(rabinovich(3))


