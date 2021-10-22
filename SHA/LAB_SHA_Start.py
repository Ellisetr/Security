import SHA_gen


def Start(input):
    print('Input message:', input)
    print('Output message:', SHA_gen.encrypt_sha(input), '\n')
