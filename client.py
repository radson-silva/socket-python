import socket, threading
#///////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////
def handle_messages(connection: socket.socket):
    #Onde vou receber as mensagens enviadas pelo servidor
    #E apresento elas no terminal do usuario
    while True:
        try:
            msg = connection.recv(1024)
            if msg:
                print(msg.decode())
            else:
                connection.close()
                break
        except Exception as e:
            print(f'Error ao manipular mensagem no servidor: {e}')
            connection.close()
            break
#///////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////
def client() -> None:
    #Processo de iniciar um cliente
    SERVER_ADDRESS = '127.0.0.1'
    SERVER_PORT = 12000

    try:
        socket_instance = socket.socket()
        socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
        # Criando uma thread para enviar mensagens ao servidor
        threading.Thread(target=handle_messages, args=[socket_instance]).start()
        print('Conexão feita com sucesso!!')

        # Lendo a entrada que o cliente digita enquanto ele não solicitar a saida
        while True:
            msg = input()
            if msg == 'sair':
                break
            socket_instance.send(msg.encode())
        socket_instance.close()

    except Exception as e:
        print(f'Erro ao se conectar com servidor {e}')
        socket_instance.close()

if __name__ == "__main__":
    client()