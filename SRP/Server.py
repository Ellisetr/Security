import random
import SHA_gen


class Server:
    def __init__(self, n, g):
        self.N = n
        self.g = g
        self.k = 3
        self.A = None
        self.B = None
        self.b = None
        self.s_s = None
        self.users = {}

    def add_user(self, info):
        self.users[info[0]] = info[1:]

    def generate_b(self, message):
        if message[1] == 0:
            raise Exception('A is 0!')
        self.A = message[1]
        self.b = random.randint(1000, 2000)
        self.B = self.k * self.users[message[0]][1] + self.g ** self.b % self.N
        return [self.B, self.users[message[0]][0]]

    def generate_server_session_key(self, username):
        self.s_s = pow(
            self.A * pow(self.users[username][1], int(SHA_gen.encrypt_sha(hex(self.A)[2:] + hex(self.B)[2:]), 16),
                         self.N), self.b, self.N)
        return self.s_s

    def compare_keys(self, key):
        if SHA_gen.encrypt_sha(str(self.A) + str(self.B) + str(self.s_s)) == key:
            print('Connection OK! Right key!')
        else:
            print('Connection end! Bad key!')
