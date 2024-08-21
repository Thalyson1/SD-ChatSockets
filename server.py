import socket

host = '192.168.2.6'
port = 8086

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(host, port)
    server.listen()
    conexao, endereco = server.accept()
    with conexao:
        print(f"Conectado {endereco}")
        while True:
            data= conexao.recv(1024)
            if not data:
                break
            conexao.sendall(data)