import codecs
from genericpath import exists
import os
import socket
import sys
import threading

HOST = 'localhost'
PORT = 8888

server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_tcp.bind((HOST, PORT))
server_tcp.listen(5)
print(f"Escutando: {HOST} \nPorta: {PORT}")
client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def conn_em_espera(conn, addr):
    print('Nova Conexão: ', addr)

'''def post_it(salvar_cache,conn):
    cache = '\n<p style="z-index:9999; position:fixed; top:20px; left:20px;width:200px;height:100px; background-color:yellow;padding:10px; font-weight:bold;">Cache: </p>'
    respostaEmString = ''
    respostaEmString = salvar_cache
    indiceDoBody = respostaEmString.find("<body>")
    novaRespostaEmString = respostaEmString[:indiceDoBody + 6] + cache + respostaEmString[indiceDoBody + 6:]
    return novaRespostaEmString'''
    

def salvar_em_cache(carregamento_pag, conn, url_Final,imag_str):
    salvar_cache = codecs.decode(carregamento_pag, encoding= 'base64')
    salvar_cacheSTR = str(salvar_cache)
    arquivo = open(url_Final+imag_str+'.txt','w')
    arquivo.write(salvar_cacheSTR)
    #arquivo.close()
    #amarelonatela = 
    #post_it(salvar_cache,conn)
    #return amarelonatela

def ler_cache(url_Final,imag_str):
    ler_arquivo = open(url_Final+imag_str,'r')
    return ler_arquivo

def conexao_browser(url_Final, url_Complexa_Divisao, urlTratamento, conn, addr,imag_str):
   
    teste_tamanho_url = (len(url_Complexa_Divisao))

    if teste_tamanho_url != 0:
        for count in range (len(url_Complexa_Divisao)-1):
            concatenar_url_complex = url_Complexa_Divisao[count]+'/'+url_Complexa_Divisao[count+1]
            concatenar_url_complexSTR = str(concatenar_url_complex)
            complemento_url = concatenar_url_complexSTR.split("'")[0]
            conexao_url = ('GET /'+complemento_url+' HTTP/1.1\r\nHost:'+url_Final+'\r\n\r\n')
    else:
        conexao_url = ('GET / HTTP/1.1\r\nHost:'+url_Final+'\r\n\r\n')
        
    client_tcp.sendall(conexao_url.encode())
    carregamento_pag = client_tcp.recv(350000)
    conn.sendall(carregamento_pag)
    print("Valor Informado: ", urlTratamento)
    thread = threading.Thread(target=conn_em_espera, args=(conn,addr))
    thread.start()
    print(f"Conexão Recebida: ", {threading.active_count() - 1})
    salvar_em_cache(carregamento_pag,conn, url_Final,imag_str)


def main():
    while True:
        conn, addr = server_tcp.accept()
        requisicao = conn.recv(350000) 
        urlTratamento = requisicao.split()[1]
        urlTratamento_STR = str(urlTratamento)
        urlTratamento_ASPAS = urlTratamento_STR.split("'")[1]
        urlTratamento_ASPAS_STR = str(urlTratamento_ASPAS)
        selec_imagem  = urlTratamento_ASPAS_STR.split(".")
        imag_str = str(selec_imagem [-1])
        urlTratamento_BARRA = urlTratamento_ASPAS_STR.split('/')[1]
        urlTratamento_BARRA_STR = str(urlTratamento_BARRA)
        url_Complexa = urlTratamento_STR.split('/')
        url_Complexa_Divisao = url_Complexa[2:]
        url_Final = urlTratamento_BARRA_STR.strip('')
        
        # Tratamento Favicon e Imagem
        if(url_Final == 'favicon.ico'):
            continue
        else:
            try:
                client_tcp.connect((url_Final,80))
            except:
                pass

        if os.path.exists(url_Final+imag_str):
            if url_Final+imag_str == '_io.TextIOWrapper':
                continue
            else:
                carregamento_do_browser= ler_cache(url_Final,imag_str)
                conn.sendall(carregamento_do_browser)
            
        else:    
            conexao_browser(url_Final, url_Complexa_Divisao, urlTratamento, conn, addr, imag_str)

if __name__ == "__main__":
    main()