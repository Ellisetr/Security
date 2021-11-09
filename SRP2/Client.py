import random
from CustomClasses import CustomHash as h

# http://srp.stanford.edu/design.html общие принципы, по которым писался код
"""
send_login_data:
    User -> Host:  I, A = g^a                  (identifies self, a = random number)
receive_login_data 
    Host -> User:  s, B = kv + g^b             (sends salt, b = random number)
calculate_scrambler:
    Both:  u = H(A, B)
calculate_session_key:
    User:  x = H(s, p)                 (user enters password)
    User:  S = (B - kg^x) ^ (a + ux)   (computes session key)
    User:  K = H(S)
Now the two parties have a shared, strong session key K. To complete authentication, they need to prove to each other that their keys match. One possible way:
calculate_m:
    User -> Host:  M = H(H(N) xor H(g), H(I), s, A, B, K)
"""


class Client:
    def __init__(self, N, g, name, password, k):
        # Простые N и g, которые получает сервер и пользователь в начале работы
        self.N = N
        self.g = g

        # Поля для хранения доп. данных
        self.A = None
        self.session_key = None
        self.a = None

        # Создание полей имени и пароля в классе пользователя
        self.name = name
        self.password = password

        # k - параметр множителя (в legacy SRP-6 дефолтно равен 3, а в SRP-6a равен хэшу N+g
        self.k = k

        # генерация "соли" случайной генерацией строки символов
        self.salt = self.generate_salt(16)

        # Создание закрытого ключа на основе соли, имени и пароля
        self.private_key = h.hash_func(str(self.salt) + self.password)

        # Создание верификатора возведением в степень g, закрытого ключа по модулю N
        self.verifier = self.generate_verifier()

        self.M = None
        self.K = None

        print("Соль пользователя", self.name, ":", hex(self.salt))
        print("Закрытый ключ пользователя: ", self.name, ":", hex(self.private_key), "\n")

    # Генерируем size-размерную соль случайным набором
    def generate_salt(self, size):
        """Метод генерации соли"""
        return int(''.join(chr(random.randint(48, 57)) for i in range(0, size)))

    # Генерация верификатора
    def generate_verifier(self):
        """Метод генерации верификатора"""
        return pow(self.g, self.private_key, self.N)

    # Отправка данных для регистрации серверу
    def send_registration_data(self):
        """Метод отправки рег.данных"""
        return [self.name, self.salt, self.verifier]

    # Отправка данных для логина серверу
    def send_login_data(self):
        """Метод отправки лог.данных"""
        self.a = random.randint(1, 1000)
        self.A = pow(self.g, self.a, self.N)
        return [self.name, self.A]

    # Получение соли (s) и B от сервера
    def receive_login_data(self, data):
        """Метод получения лог.данных"""
        s = data[0]
        B = data[1]
        self.calculate_scrambler(self.A, B)
        return self.calculate_session_key(s, B)

    def receive_m2_data(self, data):
        """Метод получения и сравнения M2"""
        M2 = h.hash_func(self.A + self.M + self.K)
        if data == M2:
            print("Клиент", self.name, ": Соединение с сервером установлено, M2 одинаковы и равны", hex(M2),"\n")
        else:
            print("Клиент", self.name, "M2 не равны, соединение разорвано \n")

    # Вычисление ключа сессии на основе соли и B, а также отправка M серверу
    def calculate_session_key(self, s, B):
        """Метод генерации открытого ключа"""
        if B != 0:
            u = self.calculate_scrambler(self.A, B)
            x = h.hash_func(str(self.salt) + self.password)
            self.session_key = pow((B - self.k * (pow(self.g, x, self.N))), (self.a + u * x), self.N)
            self.K = h.hash_func(self.session_key)
            self.M = self.calculate_m1(B, s, self.K)
            print("Ключ сессии пользователя", self.name, ":", hex(self.K),"\n")
            return self.M
        else:
            raise Exception("Клиент", self.name, ":B != 0! Соединение разорвано!")

    # Генерация M со стороны клиента
    def calculate_m1(self, B, s, K):
        """Генерация M со стороны сервера"""
        M = h.hash_func(h.hash_func(self.N) ^ h.hash_func(self.g) + s + self.A + B + K)
        return M

    # Вычислине скремблера
    def calculate_scrambler(self, A, B):
        """Генерация скремблера со стороны сервера"""
        u = h.hash_func(A + B)
        if u == 0:
            raise Exception("Разрыва соединения")
        return u
