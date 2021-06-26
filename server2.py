import socket
import sys
import datetime


ip = 'localhost'
port = 8181

timeInCache = sys.argv[1]
#----------------------------#
# Cache-Control: public
# Cache-Control: max-age=3153600
# Cache-Control: must-revalidate




def thread_client(conexao):
    print("Nova conexão: ", conexao)


def addParagraph(resposta, cache):
    #se for true, eu posso add o  POST-IT 
    # return resposta, caso contrário pois não posso add post-it a algo que não é html
    if resposta.find(b'html'):
        respostaEmString = resposta.decode()
        indiceDoBody = respostaEmString.find("<body>")
        novaRespostaEmString = respostaEmString[:indiceDoBody + 6] + cache + respostaEmString[indiceDoBody + 6:]
        return novaRespostaEmString
    else:
        return resposta

def main():

    global cached, noCache, data
    cached = ''
    noCache = ''

    arquivo = open("cache.txt","a")

    contador = 1    
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
        request = conexao.recv(5000000)

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
        print(str_dominio)
        caminhoConcatenado = ''
        print(splita_barra)
        if(len(splita_barra) == 3):
            temp = splita_barra[2]
            temp2 = temp + '/' + splita_barra[3]
            print("Linha 92")
            print('GET /{} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(temp2,str_dominio))
            server_client.send('GET /{} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(temp2,str_dominio).encode())
            print("temp2 " + temp2) 
            print("\n")
        elif(len(splita_barra) >= 4):
            for i in range(2, len(splita_barra)):
                if(i == len(splita_barra) - 1):
                    caminhoConcatenado += splita_barra[i]
                else:
                    caminhoConcatenado += splita_barra[i] + '/'
            print("Linha 102")
            print('GET /{} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(caminhoConcatenado,str_dominio))
            server_client.send('GET /{} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(caminhoConcatenado,str_dominio).encode())
            print("CaminhoConcatenado: " + caminhoConcatenado)
            print("\n")
        else:
            server_client.send('GET / HTTP/1.1\r\nHost: {}\r\n\r\n'.format(str_dominio).encode()) 

        page = server_client.recv(5000000)
        resposta = page
        #print(resposta)
        data = datetime.datetime.now()
        
        try:
            arquivo.write(resposta.decode())
        except:
            pass

        if contador != 1:
            print("está em cache")
            cached = '\n<p style="z-index:9999; position:fixed; top:20px; left:20px;width:200px;height:100px; background-color:yellow;padding:10px; font-weight:bold;">Cache: {}</p>'.format(data)
            novaRespostaComCache = addParagraph(resposta,cached)
            conexao.sendall(novaRespostaComCache.encode())
        else:
            print("Primeira vez")
            noCache = '\n<p style="z-index:9999; position:fixed; top:20px; left:20px;width:200px;height:100px; background-color:yellow;padding:10px; font-weight:bold;">Nova em: {}</p>'.format(data)
            # "resposta" está em formato de bytes
            novaRespostaSemCache = addParagraph(resposta,noCache)
            conexao.sendall(novaRespostaSemCache.encode())
        
        thread_client(conexao)
        #conexao.close()
        #ou 
        #conexao.shutdown()
        try:
            conexao.shutdown() 
        except:
            pass
        
        contador += 1 
   
        
main()
'''
http://localhost:8181/www-net.cs.umass.edu/personnel/kurose.html

'''