# The host stores passwords using the following formula:
#   x = H(s, p)               (s is chosen randomly)
#   v = g^x                   (computes password verifier)
import random

import CustomHash


class Server:
    def __init__(self, N, g, k):
        # Общие поля сервера
        self.database = {}
        self.k = k
        self.N = N
        self.g = g
        # Объявление скремблера
        self.u = None
        pass

    # Добавляем в БД имя пользователя, соль и верификатор
    def add_person(self, data):
        self.database[data[0]] = data[1], data[2]
        print("Данные пользователей в БД:", self.database)

    # Метод авторизации пользователя
    def login_person(self, data):
        if data[1] != 0:
            b = random.randint(1, 1000)
            B = (int(self.k, 16) * self.database.get(data[0])[1] + pow(self.g, b, self.N)) % self.N
            u = self.calculate_scrambler(data[1], B)
            K = self.calculate_session_key(data[1], self.database.get(data[0])[1], b, u)
            print("Ключ сессии сервера с пользователем", data[0],":",K)
            return [self.database.get(data[0])[0], B]
        else:
            raise Exception("A == 0")

    # Метод генерации открытого ключа
    def calculate_session_key(self, A, v, b, u):
        S = pow((A * pow(v, int(u, 16), self.N)), b, self.N)
        K = CustomHash.hash_func(str(S))
        return K


    def calculate_scrambler(self, A, B):
        u = CustomHash.hash_func(str(A + B))
        if u == 0:
            raise Exception("Connection aborted")
        return u
