import socket
import threading


host = '192.168.2.6'
port = 8086
SERVER = socket.gethostbyname(socket.gethostname())

server =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))


def tratar_cliente(conec, addr):
    print(f"[Nova conexão] {addr} conectado...")
    conectado = True
    while conectado:
        msg_length = conec.recv(1024).decode("UTF-8")
        if msg_length:
            msg_length = int (msg_length)
            msg= conec.recv(msg_length).decode("UTF-8")
            if msg == "sair":
                conectado = False
            print(f"[{addr}] {msg}")
        conec.send("Mensagem recebida".encode("UTF-8"))
    conec.close()

