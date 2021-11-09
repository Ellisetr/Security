from SRP2 import Client
from CustomClasses import CustomHash
from CustomClasses import CustomMath
from SRP2 import Server

def Start():
    # Генерируем N, g, и k
    # Генерируем N и g такие, что N = 2
    N = CustomMath.SafePrimeGen()
    g = CustomMath.GenMult(N)
    k = CustomHash.hash_func(str(N + g))

    # Создаём несколько пользователей, передав им N, g, имя, пароль и параметр множителя
    client = Client.Client(N, g, "Hello", "password", k)
    client2 = Client.Client(N, g, "MIREA", "qwerty", k)

    # Создаём сервер, передав ему N, g и параметр множителя
    server = Server.Server(N, g, k)

    # Регистрируем пользователей на сервере
    server.add_person(client)

    server.add_person(client2)

    # Проходим процесс аутентификации на сервере

    server.login_person(client)

    server.login_person(client2)

Start()