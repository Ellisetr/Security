from RSA import RSA_gen
import Client
import Server


def Start():
    n = RSA_gen.generate_safe_prime(100, 200)
    g = RSA_gen.calc_prim_root(n)
    server = Server.Server(n, g)
    print('Server created')
    client = Client.Client(n, g, 'ellisetr', 'qwerty')
    print('Client created')

    server.add_user(client.get_reg_data())

    a_message = client.generate_a()
    b_message = server.generate_b(a_message)

    print('Client session key is:', client.generate_session_key(b_message))
    print('Server session key is:', server.generate_server_session_key(client.get_reg_data()[0]))
    key = client.generate_key()
    server.compare_keys(key)


Start()
