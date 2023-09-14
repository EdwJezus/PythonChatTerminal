import socket
import threading

def receive_messages(client):
    while True:
        msg = client.recv(1024).decode('utf-8')
        print(msg)

server_ip = input('Digite o endereço IP do servidor: ')##PARA SER ALÉM DO LOCAL
server_port = 8888  # Porta do servidor, PARA SER ALÉM DO LOCAL

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##client.connect(('localhost', 8888))
client.connect((server_ip, server_port))

terminado = False
print('====== CHAT TERMINAL ======')
print('='*30)
print('Digite @SAIR para finalizar o chat: ')

receive_thread = threading.Thread(target=receive_messages, args=(client,))
receive_thread.start()

while not terminado:
    mensagem = input()
    client.send(mensagem.encode('utf-8'))
    if mensagem == '@SAIR':
        terminado = True

client.close()
