import random
import string
import SHA_gen


class Client:
    def __init__(self, n: int, g: int, username: str, password: str):
        self.username = username
        self.password = password
        self.N = n
        self.g = g
        self.k = 3
        self.a = None
        self.A = None
        self.B = None
        self.s_c = None
        self.s = ''.join(random.choice(string.ascii_lowercase) for i in range(random.randint(10, 15)))
        print('Salt is:', self.s)
        self.x = int(SHA_gen.encrypt_sha(self.s + self.password), 16)
        self.v = pow(self.g, self.x, self.N)

    def get_reg_data(self):
        return [self.username, self.s, self.v]

    def generate_a(self):
        self.a = random.randint(1000, 2000)
        self.A = self.g ** self.a % self.N
        return [self.username, self.A]

    def generate_session_key(self, message):
        if message[0] == 0:
            raise Exception('B is 0!')
        self.B = message[0]

        tmp1 = pow(self.g, self.x, self.N)
        tmp1 *= self.k
        tmp1 = self.B - tmp1

        tmp2 = int(SHA_gen.encrypt_sha(hex(self.A)[2:] + hex(self.B)[2:]), 16) * self.x
        self.s_c = pow(tmp1, self.a + tmp2, self.N)
        return self.s_c

    def generate_key(self):
        return SHA_gen.encrypt_sha(str(self.A) + str(self.B) + str(self.s_c))
