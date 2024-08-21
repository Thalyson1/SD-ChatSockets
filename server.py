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
            if nomeUser.startswith("!nick"):
                nomeUser = nomeUser[len("!nick"):].strip()

                with lock:
                    clientes[conec] = nomeUser
                    print(f"Nome do usuário '{nomeUser}' registrado!")
                    lista_usuarios = ' '.join(clientes.values())
                    response = f"!users {len(clientes)} {lista_usuarios}"
                    conec.sendall(response.encode('utf-8'))

            # O servidor vai receber as mensagens do usuário
            while True:
                try:
                    msg = conec.recv(1024).decode("utf-8")
                    if not msg:
                        break
                    print(f"{nomeUser} : {msg}")
                    chat_user = f"{nomeUser}: {msg}"

                    broadcast(chat_user, conec)

                except (OSError, ConnectionResetError):
                    break

        except Exception as e:
            print(f"Erro ao tratar cliente {addr}: {e}")
            
        finally:
            with lock:
                if conec in clientes:
                    del clientes[conec]
            print(f"Conexão de {addr} fechada.")
            conec.close()


def broadcast(message, exclude_conn=None):
    """Envia uma mensagem para todos os clientes conectados, exceto o especificado."""
    with lock:
        for conn in clientes:
            if conn != exclude_conn:
                try:
                    conn.sendall(message.encode('utf-8'))
                except:
                    conn.close()

def iniciar():
    server.listen()
    print(f"[Rodando...] Servidor está escutando em {SERVER}:{port}")
    while True:
        conec, addr = server.accept()
        thread = threading.Thread(target=tratar_cliente, args=(conec, addr))
        thread.start()
        print(f"[Conexões Ativas] {threading.activeCount() - 1}")

iniciar()
