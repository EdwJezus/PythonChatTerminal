import socket
import threading

def handle_client(client):
    client_address = client.getpeername()  #Obtém o endereço do cliente
    while True:
        msg = client.recv(1024).decode('utf-8')
        if msg == '@SAIR':
            clients.remove(client)
            client.close()
            print(f"Conexão encerrada por cliente {client_address}.")
            break
        else:
            print(f"{client_address}: {msg}")
            for other_client in clients:
                if other_client != client:
                    try:
                        other_client.send(f"Cliente {client_address}: {msg}".encode('utf-8'))
                    except:
                        clients.remove(other_client)
                        other_client.close()
                        print("Conexão encerrada com cliente inativo.")
                        break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 8888))
server.listen()

clients = []

print('====== CHAT TERMINAL ======')
print('='*30)
print("Servidor esperando por conexões...")

while True:
    client, client_address = server.accept()
    clients.append(client)
    print(f"Conexão estabelecida com {client_address}")

    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()

#IMPLEMENTAR
####@ORDENAR: mostra as últimas 15 mensagens, ordenadas pelo horário de envio
####@UPLOAD : faz upload de um arquivo para o servidor
####@DOWNLOAD : faz download de um arquivo do servidor
