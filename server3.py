import socket

ip = 'localhost'
port = 8181

def thread_client(conexao):
    print("Nova conexão: ", conexao)
    

def main():
    print("[*] Iniciando servidor")
    
    #SOCKET PRINCIPAL
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen(10)

    #SOCKET CLIENT
    server_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("[*] Aguardando por conexões")
    contador = 1
    while True:
        conexao, addr = server.accept()
        request = conexao.recv(8192)

        #PARTE DO TRATAMENTO PARA O FAVICON.ICO
        requisicao_favicon = request.split()
        
        #TRATAMENTO DE URL
        splita_espaco = request.split()[1]
        converte_splitespaco = str(splita_espaco)
        splita_aspas = converte_splitespaco.split("'")[1]
        converte_splitaspas = str(splita_aspas)
        splita_barra = converte_splitaspas.split('/')
        enderecopassado = converte_splitaspas.split("/")[1]
        str_dominio = str(enderecopassado)
        
        #print(str_dominio)
        #Verificação Favicon.ico

        if(str_dominio == "favicon.ico"):
            for i in requisicao_favicon:
                if len(i) > 5:
                    if((i[3:]).decode() == "p://localhost:7777/www.example.org"):
                        guardavalor = (i[3:]).decode()
                        splita_valor = guardavalor.split("/")
                        urlfinal = splita_valor[3]
                        str_dominio = urlfinal
                        server_client.connect((str_dominio, 80))
        else:
            try:
                server_client.connect((str_dominio, 80))
            except:
                pass
        
        cupenis = ''
        if(len(splita_barra) == 3):
            temp = splita_barra[2]
            temp2 = temp + '/' + splita_barra[3]
            server_client.send('GET /{} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(temp2,str_dominio).encode()) 
        elif(len(splita_barra) >= 4):
            for i in range(2, len(splita_barra)):
                if(i == len(splita_barra) - 1):
                    cupenis += splita_barra[i]
                else:
                    cupenis += splita_barra[i] + '/'
            server_client.send('GET /{} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(cupenis,str_dominio).encode()) 
        else:
            server_client.send('GET / HTTP/1.1\r\nHost: {}\r\n\r\n'.format(str_dominio).encode()) 

        page = server_client.recv(8192)
        resposta = page 
        conexao.sendall(resposta)
        thread_client(conexao)
        conexao.shutdown(socket.SHUT_RD)
        #ou 
        #conexao.shutdown()


        
'''
        conexao.sendall(str.encode("HTTP/1.0 200 OK\n",'iso-8859-1'))
        conexao.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
        conexao.sendall(str.encode('\r\n'))
        conexao.sendall(str.encode("Hello World"))
        thread_client(conexao)
        conexao.shutdown(1)
'''

main()