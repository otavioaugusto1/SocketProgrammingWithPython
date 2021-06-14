import socket


ip = 'localhost'
porta = 7777
urltratada = ''

def client(conexao, addr):
    print("[+]Nova conexão:", addr)
    connected = True

def main():
    #SOCKET PRINCIPAL
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, porta))
    server.listen(10)
    print(f"[+]Escutando no IP:",ip, "\n[+]Porta:",porta)

    #SOCKET CLIENTE QUE REQUISITA A PAGINA AO GOOGLE
    servidor_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    #ACEITA A CONEXÃO DO CLIENT
    
    while True:
        conexao, addr = server.accept()
        print("[+]Nova conexão: {}".format(addr))
        #PEGA O VALOR PASSADO NA URL
        requisicao = conexao.recv(8192)

        #NOVO TRATAMENTO
        result_new = requisicao.split()

        #FAZ O TRATAMENTO DA URL PARA PEGAR O VALOR PASSADO E TRANSFORMA EM STRING
        resultado = requisicao.split()[1]
        resultado = str(resultado)
        resultado2 = resultado.split("'")[1]
        resultado2 = str(resultado2)
        resultado_split = resultado2.split('/')
        resultado22 = resultado2.split("/")[1]
        string_resultado = str(resultado22)
        
        
        #NOVO TRATAMENTO
        if(string_resultado == 'favicon.ico'):
            for i in result_new:
                if len(i) > 5:
                    if((i[3:]).decode() == "p://localhost:7777/www.example.org"):
                        print("Achado")
                        guardavalor = (i[3:]).decode()
                        print("Valor achado:{}".format(guardavalor))
                        splita_valor = guardavalor.split("/")
                        urlfinal = splita_valor[3]
                        print("Valor final", urlfinal)
                        string_resultado = urlfinal
        else:
            servidor_client.connect((string_resultado, 80))



        #PEGA A REQUISIÇÃO E PASSA PARA O WWW.GOOGLE.COM DEPOIS TRANSFORMA EM STRING
        #servidor_client.sendall(('GET http://www.google.com/ HTTP/1.1\r\n' + 'Content-Type: application/x-www-form-urlencoded\r\n').encode())
        cupenis = ''
        if(len(resultado_split) == 3):
            temp = resultado_split[2]
            temp2 = temp + '/' + resultado_split[3]
            servidor_client.sendall('GET /{} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(temp2,string_resultado).encode()) 
        elif(len(resultado_split) >= 4):
            for i in range(2, len(resultado_split)):
                if(i == len(resultado_split) - 1):
                    cupenis += resultado_split[i]
                else:
                    cupenis += resultado_split[i] + '/'
            servidor_client.sendall('GET /{} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(cupenis,string_resultado).encode()) 
        else:
            servidor_client.sendall('GET / HTTP/1.1\r\nHost: {}\r\n\r\n'.format(string_resultado).encode()) 

        #servidor_client.sendall('GET / HTTP/1.1\r\nHost: {}\r\n\r\n'.format(string_resultado).encode()) 
        page = servidor_client.recv(8192).decode()
        #USA O SOCKET PRINCIPAL PARA ENVIAR O HTML RECEBIDO NO PAGE
        resposta = page 
        conexao.sendall(resposta.encode())
        #resposta = b"HEAD / HTTP/1.1\r\nHost: localhost\r\nAccept: text/html\r\n\r\n"
        #conexao.sendall(resposta)
        conexao.shutdown(1)
    
    



if __name__ == "__main__":
    main()