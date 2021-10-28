import socket

q = set()


def parse_links(response):
    return []


def fetch(url: str):

    sock.connect(('xkcd.com', 80))  # подключиться к сайту
    request = f'GET {url} HTTP/1.0\r\nHost: xkcd.com\r\n\r\n'

    sock.send(request.encode('ascii'))  # передать данные в сокет
    response = b''

    chunk = sock.recv(4096)  # прочитать данные из сокета
    while chunk:
        response += chunk
        chunk = sock.recv(4096)

    print(response.decode())
    # Page is now downloaded

    links = parse_links(response)
    q.update(links)


sock = socket.socket()
fetch('/')
sock.close()
