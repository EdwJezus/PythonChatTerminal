import socket
import threading
import os

#####Configuraçao recebimento de arquivos
def receive_messages(client):
    while True:
        msg = client.recv(1024).decode('utf-8')
        if msg.startswith('FILE_FOUND'):
            file_name = msg.split()[1]
            receive_file(client, file_name)
        else:
            print(msg)

######Configuração para receber comandoss
def send_commands(client):
    while True:
        command = input()
        client.send(command.encode('utf-8'))
######Configuração do comando sair do chat
        if command.upper() == '@SAIR':
            terminado = True
            print('')
            print('==================')
            print('Conexão encerrada.')
######Configuração do comando ordenar as mensagens por hora
        elif command.upper() == '@ORDENAR':
            response = client.recv(4096).decode('utf-8')
            print(response)

######Configuração para receber arqivos
def upload_file(client, file_path):
    if not os.path.exists(file_path):
        print(f'O arquivo {file_path} não existe.')
        return

    file_name = os.path.basename(file_path)
    client.send(f'@UPLOAD {file_name}'.encode('utf-8'))

    with open(file_path, 'rb') as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            client.send(data)

    print(f'Upload do arquivo {file_name} concluído.')

def download_file(client, file_name):
    client.send(f'@DOWNLOAD {file_name}'.encode('utf-8'))

def receive_file(client, file_name):
    with open(file_name, 'wb') as file:
        while True:
            data = client.recv(1024)
            if not data:
                break
            file.write(data)
    print(f'Arquivo {file_name} recebido.')

def save_file(file_name, file_data):
    with open(file_name, 'wb') as file:
        file.write(file_data)

print('====== CHAT TERMINAL ======')
print('=' * 30)
server_ip = input('Digite o endereço IP do servidor: ')
server_port = 8888

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))

terminado = False
print('=' * 30)
print('- Digite @ORDENAR para receber as últimas 15 mensagens por hora.')
print('- Digite @UPLOAD para fazer o upload de um arquivo.')
print('- Digite @DOWNLOAD para fazer o download de um arquivo.')
print('- Digite @SAIR para finalizar o chat. ')
print('=' * 30)


receive_thread = threading.Thread(target=receive_messages, args=(client,))
receive_thread.start()

send_thread = threading.Thread(target=send_commands, args=(client,))
send_thread.start()

while not terminado:
    command = input()
    if command.upper().startswith('@UPLOAD'):
        file_path = command.split()[1]
        upload_file(client, file_path)
    elif command.upper().startswith('@DOWNLOAD'):
        file_name = command.split()[1]
        download_file(client, file_name)
    else:
        client.send(command.encode('utf-8'))
        if command.upper() == '@SAIR':
            terminado = True
            print('')
            print('==================')
            print('Conexão encerrada.')

client.close()
