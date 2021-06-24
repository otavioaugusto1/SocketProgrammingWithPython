# import socket programming library
import socket

# import thread module
from _thread import *
import threading
  
print_lock = threading.Lock()
  
# thread function
def threaded(c,s,port,server_client):
    while True:
  
        # data received from client
        data = c.recv(10240)
        sendToClient(data,c,s,port,server_client)
        if not data:
            print('Bye')
              
            # lock released on exit
            print_lock.release()
            break
  
        # reverse the given string from client
        data = data[::-1]
  
        # send back reversed string to client
        
        #c.send(data) IMPORTANTE
  
    # connection closed
    c.close()
  
def sendToClient(data,c,s,port,server_client):
    requisicao_favicon = data.split()
    splita_espaco = data.split()[1]
    converte_splitespaco = str(splita_espaco)
    splita_aspas = converte_splitespaco.split("'")[1]
    converte_splitaspas = str(splita_aspas)
    splita_barra = converte_splitaspas.split('/')
    enderecopassado = converte_splitaspas.split("/")[1]
    str_dominio = str(enderecopassado)
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
    
    #server_client.connect((str_dominio,80))
    server_client.send('GET / HTTP/1.1\r\nHost: {}\r\n\r\n'.format(str_dominio).encode())
    page = server_client.recv(20480)
    c.sendall(page)
  
def main():
    host = "localhost"
  
    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 8080
    #SOCKET PRINCIPAL
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
  
    # put the socket into listening mode
    s.listen(10)
    print("socket is listening")

    #SOCKET SECUNDARIO
    server_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # a forever loop until client wants to exit
    while True:
  
        # establish connection with client
        c, addr = s.accept()
  
        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
  
        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,s,port,server_client))
    s.close()
  
  
if __name__ == '__main__':
    main()