import random
import CustomHash as h


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

        print("Соль пользователя", self.name, ":", hex(self.salt))
        print("Закрытый ключ пользователя: ", self.name, ":", hex(self.private_key), "\n")

    # Генерируем size-размерную соль случайным набором
    def generate_salt(self, size):
        return int(''.join(chr(random.randint(48, 57)) for i in range(0, size)))

    # Генерация верификатора
    def generate_verifier(self):
        return pow(self.g, self.private_key, self.N)

    # Отправка данных для регистрации серверу
    def send_registration_data(self):
        return [self.name, self.salt, self.verifier]

    # Отправка данных для логина серверу
    def send_login_data(self):
        self.a = random.randint(1, 1000)
        self.A = pow(self.g, self.a, self.N)
        return [self.name, self.A]

    # Получение соли (s) и B от сервера
    def receive_login_data(self, data):
        s = data[0]
        B = data[1]
        self.calculate_scrambler(self.A, B)
        return self.calculate_session_key(s, B)

    # Вычисление ключа сессии на основе соли и B, а также отправка M серверу
    def calculate_session_key(self, s, B):
        if B != 0:
            u = self.calculate_scrambler(self.A, B)
            x = h.hash_func(str(self.salt) + self.password)
            self.session_key = pow((B - self.k * (pow(self.g, x, self.N))), (self.a + u * x), self.N)
            K = h.hash_func(self.session_key)
            print("Ключ сессии пользователя:", self.name, ":", hex(K))
            M = self.calculate_m(B, s, K)
            return M
        else:
            raise Exception("Клиент", self.name, ":B != 0! Соединение разорвано!")

    # Генерация M со стороны клиента
    def calculate_m(self, B, s, K):
        M = h.hash_func(h.hash_func(self.N) ^ h.hash_func(self.g) + s + self.A + B + K)
        return M

    # Вычислине скремблера
    def calculate_scrambler(self, A, B):
        u = h.hash_func(A + B)
        if u == 0:
            raise Exception("Разрыва соединения")
        return u
