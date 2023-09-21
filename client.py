import socket
import threading
import os

#####Função recebimento de mensagens do servidor
def receive_messages(client):
    while True:
        msg = client.recv(1024).decode('utf-8')
        if msg.startswith('FILE_FOUND'):
            file_name = msg.split()[1]
            receive_file(client, file_name)
        else:
            print(msg)

######Função para enviar comandos para o servidor
def send_commands(client):
    while True:
        command = input()
        client.send(command.encode('utf-8'))

######Configuração do comando para sair do chat
        if command.upper() == '@SAIR':
            terminado = True
            print('')
            print('==================')
            print('Conexão encerrada.')

######Configuração do comando para ordenar as mensagens por hora
        elif command.upper() == '@ORDENAR':
            response = client.recv(4096).decode('utf-8')
            print(response)

######Configuração para fazer o upload de um arquivo para o servidor
def upload_file(client, file_path):
    if not os.path.exists(file_path):
        print(f'O arquivo {file_path} não existe.')
        return

######Obtem o nome do arquivo pelo caminho completo
    file_name = os.path.basename(file_path)
######Envia um comando para o servidor indicando o inicio do processo de upload
    client.send(f'@UPLOAD {file_name}'.encode('utf-8'))

#####Abre o arquivo local em modo binario e envia os dados pro servidor em blocos de 1024 bytes
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            client.send(data)

#####Informa que o upload do arquivo foi concluido
    print(f'Upload do arquivo {file_name} concluído.')

#######Função pra solicitar o download de um arquivo do servidor
def download_file(client, file_name):
    client.send(f'@DOWNLOAD {file_name}'.encode('utf-8'))

##########Funçao pra receber os arquivos do servidor
def receive_file(client, file_name):
#######Abre um arquivo local para escrever os dados recebidos em modo binário
    with open(file_name, 'wb') as file:
        while True:
            data = client.recv(1024)
            if not data:
                break
            file.write(data)
#####Informa que o arquivo foi recebido
    print(f'Arquivo {file_name} recebido.')


########Função pra salvar um arquivo localmente
def save_file(file_name, file_data):
    with open(file_name, 'wb') as file:
        file.write(file_data)


######Inicio de fato do programa para o cliente
print('====== CHAT TERMINAL ======')
print('=' * 30)
server_ip = input('Digite o endereço IP do servidor: ')
server_port = 8888

##########Criação do scoket do cliente e conexão com seervidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))

terminado = False
#######Menu
print('=' * 30)
print('CONECTADO COM SUCESSO!')
print('=' * 30)
print('- Digite @ORDENAR para receber as últimas 15 mensagens por hora.')
print('- Digite @UPLOAD e o caminho do arquivo para fazer o upload de um arquivo.')
print('- Digite @DOWNLOAD e o caminho do arquivo para fazer o download de um arquivo.')
print('- Digite @SAIR para finalizar o chat. ')
print('=' * 30)

####Thread para receber mensagens do servidor
receive_thread = threading.Thread(target=receive_messages, args=(client,))
receive_thread.start()

####Thread para enviar comando pro servidor
send_thread = threading.Thread(target=send_commands, args=(client,))
send_thread.start()

while not terminado:
    command = input()
######Verifica se o comando começa com @UPLOAD para fazer upload de um arquivo
    if command.upper().startswith('@UPLOAD'):
        file_path = command.split()[1]
        upload_file(client, file_path)
########Verifica se o comando começa com @DOWNLOAD para solicitar o download de um arquivo
    elif command.upper().startswith('@DOWNLOAD'):
        file_name = command.split()[1]
        download_file(client, file_name)
    else:
#########Envia o comando para o servidor
        client.send(command.encode('utf-8'))
######Verifica se o comando é para sair do chat
        if command.upper() == '@SAIR':
            terminado = True
            print('')
            print('==================')
            print('Conexão encerrada.')

###Fecha o socket do cliente após sair do loop
client.close()
