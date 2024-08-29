import socket

import threading

import re




host = '25.51.113.214'

port= 8086






client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((host, port))




def enviar_msg():

   #client vai enviar o nome

   try:

       nomeUser = input("Digite seu nick: ")

       comando_nick = f"!nick {nomeUser}"

       print(f"Enviando comando: {comando_nick}")

       client.send(comando_nick.encode('utf-8'))






       #função threading para ficar recebendo dados do servidor sempre que tiver att.

       def receber_do_server():

           while True:

               try:

                   #pega os dados

                   response = client.recv(1024).decode('utf-8')

                   

                   if not response:

                       print("Conexão fechada")

                       break

                   #mostra a(s) mensagem(s) do(s) usuário(s)

                   print(f"\n{response}")

               except:

                   print("error")

                   break

       #aqui mostra os usuários que estão conectados       

       response_Users = client.recv(1024).decode('utf-8')

       print(f"Usuários conectados: {response_Users}")

       threading.Thread(target=receber_do_server, daemon=True).start()




       #receber a msg e tratamento para sair da aplicação

       while True:

           msg = input("Digite uma mensagem: \n")

           if msg.lower() == 'sair':

               break


           if re.match(r"^!poke", msg):

               client.send(msg.encode())

               
           elif re.match(r"^!changenickname", msg):

               client.send(msg.encode())
 

           else:

               client.send(f"!sendmsg {msg}".encode('utf-8'))






   finally:

       client.close()

       

enviar_msg()