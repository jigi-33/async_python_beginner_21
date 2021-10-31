import socket

# Видео 1 от Молчанова О.
#
# Понять вообще про сокеты.
# socket - пара domain:port
# Понять о блокирующих операциях.
# Понять о контроле выполнения программы в виде кода.
#
# event loop - событийный цикл, одно из ключевых понятий в асинхронности.
#
# Асинхронный код можно писать без использования сторонних библиотек следующими способами:
# 1. С пом. callback'ов  2. С пом. генераторов и корутин  3. С пом. синтаксиса async - await
#
# Все эти способы мы промоделируем в следующих видео...


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 1 is True
server_socket.bind(('localhost', 5001))
server_socket.listen()

while True:
    print('Before .accept()')
    client_socket, addr = server_socket.accept()  # читает данные со входящего буфера и возвращает кортеж (клентский сокет и адрес)
    print('Connection from', addr)

    while True:  # дожидаемся от клиента текстового сообщения
        print('Before .recv()')
        request = client_socket.recv(4096)  # размер буфера сообщения, в кб

        if not request:  # условие для прерывания цикла
            break
        else:
            response = 'Hello world\n'.encode()  # ответ со стороны сервера на запрос
            client_socket.send(response)

    print('Outside inner while loop\n')
    client_socket.close()
