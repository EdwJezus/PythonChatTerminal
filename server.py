import socket
import threading
from datetime import datetime
import os

#######Lista para armazenar mensagens
mensagens = []

###########Função pra lidar com clietes
def handle_client(client):
########Obtem o endereco do cliente
    client_address = client.getpeername()

    while True:
###########Recebe uma mensagem do cliente
        msg = client.recv(1024).decode('utf-8')

#########Comando pro cliente sair do chat
        if msg.upper() == '@SAIR':
            clients.remove(client)
            client.close()
            print(f'Conexão encerrada por cliente {client_address}.')
            break

#########Comando para receber as mesagens em ordem por hora
        elif msg.upper() == '@ORDENAR':
            ordem_mensagens = sorted(mensagens, key=lambda x: x[1])
            response = ""
            for mensagem, hora, sender_address in ordem_mensagens[-15:]:
                response += f'{sender_address} {hora}:: {mensagem}\n'
            client.send(response.encode('utf-8'))

#########Comando para fazer upload
        elif msg.upper().startswith('@UPLOAD'):
            file_name = msg.split()[1]
            receive_file(client, file_name)

###########Comando para fazer download
        elif msg.upper().startswith('@DOWNLOAD'):
            file_name = msg.split()[1]
            send_file(client, file_name)

        else:
#############Obtem a hora atual
            hora = datetime.now().strftime('%H:%M:%S')
##########Armazena a mensagem na lista de mensagens
            mensagens.append((msg, hora, client_address))

#########Envio de mensagens para outros clientes
            print(f'{client_address}: {msg}')
            for other_client in clients:
                if other_client != client:
                    try:
                        other_client.send(f'Cliente {client_address}: {msg}'.encode('utf-8'))
#######Desconexão do cliente
                    except:
                        clients.remove(other_client)
                        other_client.close()
                        print('Conexão encerrada com cliente inativo.')
                        break

#######Recebimento de arquivos
def receive_file(client, file_name):
    with open(file_name, 'wb') as file:
        while True:
            data = client.recv(1024)
            if not data:
                break
            file.write(data)
    print(f'Arquivo {file_name} recebido.')

#######Envio de arquivos
def send_file(client, file_name):
    if os.path.exists(file_name):
#######Envia um sinal para o cliente indicando que o arquivo foi encontrado
        client.send(f'FILE_FOUND {file_name}'.encode('utf-8'))

#####Abre o arquivo e envia os dados pro cliente em blocos de 1024 bytes
        with open(file_name, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                client.send(data)

#######Informa que o arquivo foi enviado
        print(f'Arquivo {file_name} enviado para download.')
    else:
#####Se o arquivo nao for encontrado ele envia uma mensagem de erro pro cliente
        client.send('FILE_NOT_FOUND'.encode('utf-8'))
        print(f'O arquivo {file_name} não foi encontrado no servidor.')

######Condiguração socket e endereço
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '0.0.0.0'
server_port = 8888
server.bind((server_ip, server_port))
server.listen()

########Lista de clientes conectados
clients = []

#######Menu
print('====== CHAT TERMINAL ======')
print('=' * 30)
print('Servidor esperando por conexões...')

######Conexão com clientes
while True:
    client, client_address = server.accept()
    clients.append(client)
    print(f'Conexão estabelecida com {client_address}')

#######Cria uma nova thread para lidar com o cliente
    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()
