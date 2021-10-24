import random
import CustomHash


# http://srp.stanford.edu/design.html общие принципы, по которым писался код

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
        self.private_key = CustomHash.hash_func(self.salt + self.password)

        # Создание верификатора возведением в степень g, закрытого ключа по модулю N
        self.verifier = self.generate_verifier()

        print("Соль пользователя: ",self.salt)
        print("Закрытый ключ пользователя: ",self.private_key)

    # Генерируем size-размерную соль случайным набором букв и чисел
    def generate_salt(self, size):
        return ''.join(chr(random.randint(48, 57)) for i in range(0, size))

    # Генерация верификатора
    def generate_verifier(self):
        return pow(self.g, int(self.private_key, 16), self.N)

    # Отправка данных для регистрации
    def send_registration_data(self):
        return [self.name, self.salt, self.verifier]

    # Отправка данных для логина серверу
    def send_login_data(self):
        self.a = random.randint(1,1000)
        self.A = pow(self.g, self.a, self.N)
        return [self.name, self.A]

    # Получение соли (s) и B от сервера
    def receive_login_data(self, data):
        s = data[0]
        B = data[1]
        self.calculate_scrambler(self.A, B)
        self.calculate_session_key(s, B)

    # Вычисление ключа сессии на основе соли и B
    def calculate_session_key(self, s, B):
        if B != 0:
            u = self.calculate_scrambler(self.A, B)
            x = CustomHash.hash_func(self.salt + self.password)
            self.session_key = pow((B - int(self.k,16) * (pow(self.g, int(x,16), self.N))), (self.a + u * int(x,16)), self.N)
            K = CustomHash.hash_func(str(self.session_key))
            print("Ключ сессии пользователя:",K)

    # Вычислине скремблера
    def calculate_scrambler(self, A, B):
        u = int(CustomHash.hash_func(str(A + B)), 16)
        if u == 0:
            raise Exception("Connection aborted")
        return u
