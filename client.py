import socket
import threading

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

        def receber_do_server():
            while True:
                try:
                    response = client.recv(1024).decode('utf-8')
                    
                    if not response:
                        print("Conexão fechada")
                        break
                    print(f"\n{response}")
                except:
                    print("error")
                    break
        response_Users = client.recv(1024).decode('utf-8')
        print(f"Usuários conectados: {response_Users}")
        threading.Thread(target=receber_do_server, daemon=True).start()

        while True:
            msg = input("Digite uma mensagem: \n")
            if msg.lower() == 'sair':
                break
            client.send(msg.encode('utf-8'))


    finally:
        client.close()
        
enviar_msg()