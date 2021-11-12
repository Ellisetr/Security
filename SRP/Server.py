import random
from CustomClasses import CustomHash as h

"""
http://srp.stanford.edu/design.html общие принципы, по которым писался код
Методы и то, что они выполняют по принципам SRP
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
calculate_m1:
    User -> Host:  M1 = H(H(N) xor H(g), H(I), s, A, B, K)
    Host -> User:  M2 = H(A, M, K)
"""


class Server:
    def __init__(self, N, g, k):
        # Общие поля сервера
        self.database = {}
        self.k = k
        self.N = N
        self.g = g

    def add_person(self, Client_obj):
        """Добавляет в БД имя пользователя, соль и верификатор"""
        data = Client_obj.send_registration_data()
        self.database[data[0]] = hex(data[1]), hex(data[2])
        print("Данные пользователей в БД:", self.database, "\n")

    def login_person(self, Client_obj):
        """Метод авторизации пользователя"""
        # Получаем запрос на вход от клиента
        data = Client_obj.send_login_data()

        if data[1] != 0 and data[0] in self.database:
            b = random.randint(1, 1000)
            B = (self.k * int(self.database.get(data[0])[1], 16) + pow(self.g, b, self.N)) % self.N
            u = self.calculate_scrambler(data[1], B)
            K = self.calculate_session_key(data[1], int(self.database.get(data[0])[1], 16), b, u)
            print("Ключ сессии сервера с пользователем", data[0], ":", hex(K))

            # Отправляем данные, для генерации M1 и получаем M1 от клиента
            usr_M1 = Client_obj.receive_login_data([int(self.database.get(data[0])[0], 16), B])
            M1 = self.calculate_m1(B, int(self.database.get(data[0])[0], 16), K, data[1])

            # Сравниваем M1 клиента и сервера
            if M1 == usr_M1:
                M2 = h.hash_func(data[1] + M1 + K)
                print("Сервер: Попытка соединения с", data[0], ", M1 одинаковы и равны:", hex(M1))
                # Отправляем M2 для верификации на стороне клиента
                Client_obj.receive_m2_data(M2)
            else:
                raise Exception("Сервер: M1 не равны! Разрыв соединения с", data[0],"!")
        else:
            raise Exception("Сервер: A == 0 или клиент не существует в БД! Соединение разорвано!")

    def calculate_session_key(self, A, v, b, u):
        """Метод генерации открытого ключа"""
        S = pow((A * pow(v, u, self.N)), b, self.N)
        K = h.hash_func(str(S))
        return K

    def calculate_m1(self, B, s, K, A):
        """Генерация M1 со стороны сервера"""
        M1 = h.hash_func(h.hash_func(self.N) ^ h.hash_func(self.g) + s + A + B + K)
        return M1

    def calculate_scrambler(self, A, B):
        """Генерация скремблера со стороны сервера"""
        u = h.hash_func(str(A + B))
        if u == 0:
            raise Exception("Сервер: U == 0! Разрыв соединения!")
        return u
