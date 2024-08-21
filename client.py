import socket

host = '192.168.2.6'
port= 8086


client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def enviar_msg():
    try:
        nomeUser = input("Digite seu nick: ")
        client.send(f"!nick {nomeUser}".encode('utf-8'))

        response = client.recv(1024).decode('utf-8')

        while True:
            msg = input("Digite uma mensagem: ")
            if msg.lower() == 'sair':
                break
            client.send(msg.encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            print(f"Resposta do server: {response}")

    finally:
        client.close()
        
enviar_msg()