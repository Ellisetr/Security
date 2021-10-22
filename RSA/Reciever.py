import RSA_gen


class Receiver:
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.module = self.p * self.q
        self.f = RSA_gen.eulerFunction(self.p, self.q)
        self.e = RSA_gen.generateOpenExponent(self.f)
        self.public_key = [self.e, self.module]
        self.private_key = [self.secretKeyCorrection(list(self.secretKeyGen(self.e, self.f))[1]), self.module]
        print('Public key are:', self.public_key, 'Private key are:', self.private_key)

    def decryptMessage(self, encrypted_text):
        output = ''
        for character in encrypted_text:
            output += chr(character ** self.private_key[0] % self.private_key[1])
        return output

    def secretKeyGen(self, a, b):
        if a == 0:
            return b, 0, 1
        gcd, xn, yn = self.secretKeyGen(b % a, a)
        x = yn - (b // a) * xn
        y = xn
        return gcd, x, y

    def secretKeyCorrection(self, secret_key):
        if secret_key >= 0:
            return secret_key
        return self.f + secret_key
