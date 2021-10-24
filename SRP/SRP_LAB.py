import Client
import CustomHash
import Server

# Генерируем N, g, и k
N = 1337
g = 1488
k = CustomHash.hash_func(str(N + g))

# Создаём несколько пользователей, передав им N, g, имя, пароль и параметр множителя
client = Client.Client(N, g, "Hello", "password", k)
client2 = Client.Client(N, g, "Nikita", "qwerty", k)

# Создаём сервер, передав ему N, g и параметр множителя
server = Server.Server(N, g, k)

# Регистрируем пользователей на сервере
server.add_person(client.send_registration_data())
server.add_person(client2.send_registration_data())

# Проходим процесс аутентификации на сервере
client.receive_login_data(server.login_person(client.send_login_data()))
client2.receive_login_data((server.login_person(client2.send_login_data())))
