import socket
import threading

host = '192.168.2.6'
port = 8086
SERVER = socket.gethostbyname(socket.gethostname())

clientes = {}
lock = threading.Lock()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

def tratar_cliente(conec, addr):
    with conec:
        print(f"[Nova conexão] {addr} conectado...")

        try:
            # Recebe o nome do cliente
            nomeUser = conec.recv(1024).decode('utf-8')

            #tratamento da tag
            if not nomeUser.startswith("!nick"):
                print("Error, você deve enviar seu nickname primeiro '!nick nome'. \nServidor fechado...")
                conec.close()
            else:
                nomeUser = nomeUser[len("!nick"):].strip()

                #Crie uma lista para inserir todos os users e dps mostrar eles para os usuários novos.
                with lock:
                    clientes[conec] = nomeUser
                    print(f"Nome do usuário '{nomeUser}' registrado!")
                    lista_usuarios = ' '.join(clientes.values())
                    response = f"!users {len(clientes)} {lista_usuarios}"
                    conec.sendall(response.encode('utf-8'))

            # O servidor vai receber as mensagens do usuário
            while True:
                try:
                    #devo iniciar +- aqui o tratamento de mensagens com a tag !send
                    msg = conec.recv(1024).decode("utf-8")

                    if msg.startswith("!sendmsg"):

                        msg = msg[len("!sendmsg"):].strip()
                        print(f"!msg {nomeUser} : {msg}")
                        chat_user = f"{nomeUser}: {msg}"
                        broadcast(chat_user, conec)


                    elif msg.startswith("!changenickname"):
                        nomeUserstate = nomeUser
                        newNomeUser = msg[len("!changenickname"):].strip()

                        if newNomeUser:
                            nomeUser= newNomeUser
                            broadcast(f"{nomeUserstate} trocou o nome para {nomeUser}\n")
                        else:
                            conec.send("Error: falha ao atualizar nome")
                        
                    else:
                        broadcast(f"Error, {nomeUser} você deve informar a tag '!sendmsg' para enviar uma mensagem ou '!changenickname para trocar o nome', tente novamente\n")
                        
                    
                except:
                    break

        #caso naão dê certo, fechar conexão
        finally:
            with lock:
                if conec in clientes:
                    del clientes[conec]
            print(f"Conexão {addr} fechada.")
            conec.close()


def broadcast(message, exclude_conn=None):
    #Envia uma mensagem para todos os clientes conectados, exceto o próprio user.
    with lock:
        for conn in clientes:
            if conn != exclude_conn:
                try:
                    conn.sendall(message.encode('utf-8'))
                except:
                    conn.close()
                    if conn in clientes:
                        del clientes[conn]


def iniciar():
    server.listen()
    print(f"[Rodando...] Servidor está escutando em {SERVER}:{port}")
    while True:
        conec, addr = server.accept()
        thread = threading.Thread(target=tratar_cliente, args=(conec, addr))
        thread.start()
        print(f"[Conexões Ativas] {threading.activeCount() - 1}")

iniciar()
