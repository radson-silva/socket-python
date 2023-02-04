import socket, threading
connections = []

# Define o gabarito de questões no servidor
gabarito = {
    1: "VVVV",
    2: "FVFV",
    3: "VFVV",
    4: "VVFV",
    5: "FVVF"
}


def handle_user_connection(connection: socket.socket, address: str) -> None:
    #Pega a conexão dos usuarios e envia para os conectados
        
    while True:
        try:
            # Captura o input da mensagem
            dados = connection.recv(1024)
            if dados:
                print(f"=======================")
                print(f"{dados}")
                dados = dados.decode()
                questao, alternativa, resposta = dados.split(';')
                questao = int(questao)
                alternativa = int(alternativa)
                print(f"{questao}")
                print(f"{resposta}")
                num_acertos = sum(a == b for a, b in zip(resposta, gabarito[questao]))
                num_erros = alternativa - num_acertos
                print(f"{questao};Acertos [{num_acertos}]; Erros[{num_erros}]")
                msg_to_send = (f"{questao};Acertos [{num_acertos}]; Erros[{num_erros}]")
                broadcast(msg_to_send, connection)
            else:
                remove_connection(connection)
                break

        except Exception as e:
            print(f'Erro ao enviar mensagem: {e}')
            remove_connection(connection)
            break

def broadcast(message: str, connection: socket.socket) -> None:
    #Disparo brodcast, para todos os usuarios
    for client_conn in connections:
        if client_conn == connection:
            try:
                client_conn.send(message.encode())
            except Exception as e:
                print('Erro ao enviar a mensagem: {e}')
                remove_connection(client_conn)

def remove_connection(conn: socket.socket) -> None:
    if conn in connections:
        conn.close()
        connections.remove(conn)

def server() -> None:
    LISTENING_PORT = 12000
    
    try:
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(('', LISTENING_PORT))
        socket_instance.listen(4)

        print('Servidor Iniciado com sucesso!!!')
        
        while True:
            #Iniciando nova thread no servidor
            socket_connection, address = socket_instance.accept()
            connections.append(socket_connection)
            threading.Thread(target=handle_user_connection, args=[socket_connection, address]).start()

    except Exception as e:
        print(f'Erro ao criar a nova thread: {e}')
    finally:
        # Limpar todas as conexões em caso de problema no servidor
        if len(connections) > 0:
            for conn in connections:
                remove_connection(conn)
        socket_instance.close()


if __name__ == "__main__":
    server()