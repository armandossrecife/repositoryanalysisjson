# Consumidor e Produtor
# Consumidor da fila 'fila_banco'
# Produtor na fila 'fila_repositorio_local'

# 1. Operacões no Banco de Dados
# produtor_salva_banco
# fila_banco
# consumidor_salva_banco

# 1.1. Dispara uma solicitação para salvar o repositório no BD (1)
# 1.2. Enfilera solicitação na fila (2) (produtor)
# 1.3. Consome da fila de operações do BD (3) (consumidor)
# 1.4. Repositório salvo no BD (4)

# 2. Operações de clonagem do repositório
# produtor_clona_repositorio
# fila_repositorio_local
# consumidor_clona_repositorio

# 2.1. Dispara uma solicitação para clonar o repositório no sistema de arquivo local (5)
# 2.2. Enfilera pedido de clonagem do repositório (6) (produtor)
# 2.3. Consome da fila de operações de clonagem (7) (consumidor)
# 2.4. Repositório clonado no sistema de arquivos local (8)

import pika
from git import Repo
import os
 
rabbitmq_broker_host = 'localhost'
my_fila1 = 'fila_banco'
my_fila2 = 'fila_repositorio_local'
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_broker_host))

channel_salva_banco = connection.channel()
channel_salva_banco.queue_declare(queue=my_fila1, durable=True)

channel_to_clone = connection.channel() 
channel_to_clone.queue_declare(queue=my_fila2, durable=True)

# 2.2. Enfilera pedido de clonagem do repositório (6) (produtor)
def msg_clona_repositorio(canal=channel_to_clone, fila=my_fila2, usuario='', repositorio=''):
    print(f'Conectando ao canal channel_to_clone na fila {fila}')
    print(f'Enviando o pedido de clonagem do repositório {repositorio}')
    conteudo = 'user=' + usuario + ',' + 'repository=' + repositorio
    canal.basic_publish(exchange='', routing_key=fila, body=conteudo)

# 1.3. Consome da fila de operações do BD (3) (consumidor)
def salva_no_banco_callback(ch, method, properties, body):
    body = body.decode('utf-8')
    if 'user' in body:
        try:
            str_temp = body.split(',')
            user = str_temp[0].split('=')[1]
            repositorio = str_temp[1].split('=')[1]       
            separa_ponto = repositorio.split('.')
            nome_repositorio_temp = separa_ponto[1]
            nome_repositorio = nome_repositorio_temp.split('/')[-1]
            repo_dir = nome_repositorio
            if not os.path.isdir(repo_dir):
                try:
                    # 1.4. Repositório salvo no BD (4)
                    print(f'Operação de salvar o {repositorio} no Banco')
                    print(f'Repositório {nome_repositorio} salvo no BD com sucesso!')
                    # 2.1. Dispara uma solicitação para clonar o repositório no sistema de arquivo local (5)
                    msg_clona_repositorio(canal=channel_to_clone, fila=my_fila2, usuario=user, repositorio=repositorio)
                except Exception as ex:
                    print(f'Erro: {str(ex)}')
            else:
                print(f'O repositório {repositorio} já foi clonado no diretório {repo_dir}')
        except Exception as ex:
            print(f'Erro: {str(ex)}')     
 
channel_salva_banco.basic_consume(my_fila1, salva_no_banco_callback, auto_ack=True)
 
print(' [*] Waiting for messages to save repository in BD. To exit press CTRL+C')
channel_salva_banco.start_consuming()