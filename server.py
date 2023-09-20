import socket
import threading
from datetime import datetime

mensagens = []

def handle_client(client):
    client_address = client.getpeername()
    while True:
        msg = client.recv(1024).decode('utf-8')
        if msg.upper() == '@SAIR':
            clients.remove(client)
            client.close()
            print(f'Conexão encerrada por cliente {client_address}.')
            break
        elif msg.upper() == '@ORDENAR':
            ordem_mensagens = sorted(mensagens, key=lambda x: x[1])
            response = ""
            for mensagem, hora, sender_address in ordem_mensagens[-15:]:
                response += f'{sender_address} {hora}:: {mensagem}\n'
            client.send(response.encode('utf-8'))
        else:
            hora = datetime.now().strftime('%H:%M:%S')
            ##timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            mensagens.append((msg, hora, client_address))
            print(f'{client_address}: {msg}')
            for other_client in clients:
                if other_client != client:
                    try:
                        other_client.send(f'Cliente {client_address}: {msg}'.encode('utf-8'))
                    except:
                        clients.remove(other_client)
                        other_client.close()
                        print('Conexão encerrada com cliente inativo.')
                        break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '0.0.0.0'
server_port = 8888
server.bind((server_ip, server_port))
server.listen()

clients = []

print('====== CHAT TERMINAL ======')
print('=' * 30)
print('Servidor esperando por conexões...')

while True:
    client, client_address = server.accept()
    clients.append(client)
    print(f'Conexão estabelecida com {client_address}')

    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()

#IMPLEMENTAR
####@UPLOAD : faz upload de um arquivo para o servidor
####@DOWNLOAD : faz download de um arquivo do servidor
