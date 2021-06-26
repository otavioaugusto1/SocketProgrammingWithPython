import codecs
from genericpath import exists
import os
import socket
import sys
import threading
import datetime

ip = 'localhost'
port = 8888
data = datetime.datetime.now()

#Pegando o tempo em cache
timeInCache = sys.argv[1]
#-----------------------


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen(5)
print(f"Escutando: {ip} \nporta: {port}")
server_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def conexao_em_espera(conexao, addr):
    print('Nova Conexão: ', addr)


def post_it(salvar_cache):
    no_cache = '\n<p style="z-index:9999; position:fixed; top:20px; left:20px;width:200px;height:100px; background-color:yellow;padding:10px; font-weight:bold;">Novo: {}</p>'.format(data)
    if salvar_cache.find(b'html'):
        respostaEmString = salvar_cache.decode()
        indiceDoBody = respostaEmString.find("<body>")
        novaRespostaEmString = respostaEmString[:indiceDoBody + 6] + no_cache + respostaEmString[indiceDoBody + 6:]
        print(novaRespostaEmString)
        if novaRespostaEmString.find("Cache-Control: max-age=604800"):
            novaRespostaEmString = novaRespostaEmString.replace("Cache-Control: max-age=604800","Cache-Control: max-age=120")
            print(novaRespostaEmString)
        return novaRespostaEmString
    else:
        return salvar_cache
   

def salvar_em_cache(carregamento_pag, conexao, str_dominio,imag_str):
    salvar_cache = codecs.decode(carregamento_pag, encoding= 'base64')
    salvar_cacheSTR = str(salvar_cache)
    arquivo = open(str_dominio+imag_str+'.txt','w')
    arquivo.write(salvar_cacheSTR)
    #arquivo.close()
    #amarelonatela = 
    #post_it(salvar_cache,conexao)
    #return amarelonatela

def ler_cache(str_dominio,imag_str):
    ler_arquivo = open(str_dominio+imag_str,'r')
    return ler_arquivo

def conexao_browser(str_dominio, url_Complexa_Divisao, urlTratamento, conexao, addr,imag_str):
   
    teste_tamanho_url = (len(url_Complexa_Divisao))

    if teste_tamanho_url != 0:
        for count in range (len(url_Complexa_Divisao)-1):
            concatenar_url_complex = url_Complexa_Divisao[count]+'/'+url_Complexa_Divisao[count+1]
            concatenar_url_complexSTR = str(concatenar_url_complex)
            complemento_url = concatenar_url_complexSTR.split("'")[0]
            conexao_url = ('GET /'+complemento_url+' HTTP/1.1\r\nHost: '+str_dominio+'\r\n\r\n')
    else:
        conexao_url = ('GET / HTTP/1.1\r\nHost: '+str_dominio+'\r\n\r\n')
        
    server_client.sendall(conexao_url.encode())
    carregamento_pag = server_client.recv(350000)
    carregamento_pag_com_post_it = post_it(carregamento_pag)
    conexao.sendall(carregamento_pag_com_post_it.encode())
    print("Valor Informado: ", urlTratamento)
    thread = threading.Thread(target=conexao_em_espera, args=(conexao,addr))
    thread.start()
    print(f"Conexão Recebida: ", {threading.active_count() - 1})
    salvar_em_cache(carregamento_pag,conexao, str_dominio,imag_str)


def main():
    while True:
        #tratamento do corpo da URL
        conexao, addr = server.accept()
        requisicao = conexao.recv(350000) 
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
        str_dominio = urlTratamento_BARRA_STR.strip('')
        
        # Tratamento Favicon e Imagem
        if(str_dominio == 'favicon.ico'):
            continue
        else:
            try:
                server_client.connect((str_dominio,80))
            except:
                pass

        if os.path.exists(str_dominio+imag_str):
            if str_dominio+imag_str == '_io.TextIOWrapper':
                continue
            else:
                carregamento_do_browser= ler_cache(str_dominio,imag_str)
                conexao.sendall(carregamento_do_browser)     
        else:    
            conexao_browser(str_dominio, url_Complexa_Divisao, urlTratamento, conexao, addr, imag_str)

if __name__ == "__main__":
    main()