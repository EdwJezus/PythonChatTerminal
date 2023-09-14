import socket
import threading

def receive_messages(client):
    while True:
        msg = client.recv(1024).decode('utf-8')
        print(msg)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8888))

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
