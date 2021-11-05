import random
import CustomHash as h

"""
The host stores passwords using the following formula:
  x = H(s, p)               (s is chosen randomly)
  v = g^x                   (computes password verifier)
The host then keeps {I, s, v} in its password database. The authentication protocol itself goes as follows:

add_person:
User -> Host:  I, A = g^a                  (identifies self, a = random number)

login_person:
    Host -> User:  s, B = kv + g^b             (sends salt, b = random number)
calculate_scrambler:
    Both:  u = H(A, B)
calculate_session_key: 
    Host:  S = (Av^u) ^ b              (computes session key)
    Host:  K = H(S)
    Now the two parties have a shared, strong session key K. To complete authentication, they need to prove to each other that their keys match. One possible way:
calculate_m:
    User -> Host:  M = H(H(N) xor H(g), H(I), s, A, B, K)
    Host -> User:  H(A, M, K)
"""

class Server:
    def __init__(self, N, g, k):
        # Общие поля сервера
        self.database = {}
        self.k = k
        self.N = N
        self.g = g

    # Добавляем в БД имя пользователя, соль и верификатор
    def add_person(self, Client_obj):
        data = Client_obj.send_registration_data()
        self.database[data[0]] = data[1], data[2]
        print("Данные пользователей в БД:", self.database)

    # Метод авторизации пользователя
    def login_person(self, Client_obj):
        # Получаем запрос на вход от клиента
        data = Client_obj.send_login_data()

        if data[1] != 0 and data[0] in self.database:
            b = random.randint(1, 1000)
            B = (self.k * self.database.get(data[0])[1] + pow(self.g, b, self.N)) % self.N

            u = self.calculate_scrambler(data[1], B)

            K = self.calculate_session_key(data[1], self.database.get(data[0])[1], b, u)
            print("Ключ сессии сервера с пользователем", data[0], ":", hex(K))

            # Отправляем данные, для генерации M и получаем M от клиента
            usr_M = Client_obj.receive_login_data([self.database.get(data[0])[0], B])

            M = self.calculate_m(B, self.database.get(data[0])[0], K, data[1])

            # Сравниваем M клиента и сервера
            if M == usr_M:
                R = h.hash_func(data[1] + M + K)
                print("Сервер: Соединение установлено, M одинаковы и равны:", hex(M), "; R равен:", hex(R), "\n")
            else:
                raise Exception("Сервер: K не равны! Разрыв соединения с", data[0])
        else:
            raise Exception("Сервер: A == 0 или клиент не существует в БД! Соединение разорвано!")

    # Метод генерации открытого ключа
    def calculate_session_key(self, A, v, b, u):
        S = pow((A * pow(v, u, self.N)), b, self.N)
        K = h.hash_func(str(S))
        return K

    # Генерация M со стороны сервера
    def calculate_m(self, B, s, K, A):
        M = h.hash_func(h.hash_func(self.N) ^ h.hash_func(self.g) + s + A + B + K)
        return M

    # Генерация скремблера со стороны сервера
    def calculate_scrambler(self, A, B):
        u = h.hash_func(str(A + B))
        if u == 0:
            raise Exception("Сервер: Соединение разорвано")
        return u
