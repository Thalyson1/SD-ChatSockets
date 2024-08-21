import socket

host = '192.168.2.6'
port= 8086


client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def enviar_msg():
    try:
        nomeUser = input("Digite seu nick: ")
        comando_nick = f"{nomeUser}"
        print(f"Enviando comando: {comando_nick}")
        client.send(comando_nick.encode('utf-8'))

        response = client.recv(1024).decode('utf-8')
        print(f"Lista de usuários conectados: {response}")
        
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