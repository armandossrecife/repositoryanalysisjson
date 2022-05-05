# Consumidor e Produtor
# Consumidor da fila 'fila_repositorio_local'
# Produtor na fila 'fila_status_banco'

# 2. Operações de clonagem do repositório
# produtor_clona_repositorio (consumidor_salva_repositorio)
# fila_repositorio_local (ok)
# consumidor_clona_repositorio

# 2.1. Dispara uma solicitação para clonar o repositório no sistema de arquivo local (5)
# 2.2. Enfilera pedido de clonagem do repositório (6) (produtor)
# 2.3. Consome da fila de operações de clonagem (7) (consumidor)
# 2.4. Repositório clonado no sistema de arquivos local (8)

# 3. Operação de atualizar Banco de Dados 
# produtor_atualiza_status_banco
# fila_status_banco
# consumidor_atualiza_status_banco

# 3.1. Dispara uma solicitação para atualizar o status do repositório no BD (9)
# 3.2. Enfilera pedido de atualização do status do repositório no BD (10) (produtor)
# 3.3. Consome da fila de status do BD (11) (consumidor)
# 3.4. Repositório com status atualizado para clonado no BD (12)

import pika
from git import Repo
import os
 
rabbitmq_broker_host = 'localhost'
my_fila1 = 'fila_repositorio_local'
my_fila2 = 'fila_status_banco'

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_broker_host))

channel_to_clone = connection.channel()
channel_to_clone.queue_declare(queue=my_fila1, durable=True)

channel_to_update_db = connection.channel() 
channel_to_update_db.queue_declare(queue=my_fila2, durable=True)

# 3.2. Enfilera pedido de atualização do status do repositório no BD (10) (produtor)
def msg_update_db_repositorio(canal=channel_to_update_db, fila=my_fila2, usuario='', repositorio=''):
    print(f'Conectando ao canal channel_to_update_db na fila {fila}')
    print(f'Enviando o pedido de update do repositório {repositorio} no BD')
    conteudo = 'user=' + usuario + ',' + 'repository=' + repositorio
    canal.basic_publish(exchange='', routing_key=fila, body=conteudo)

# 2.3. Consome da fila de operações de clonagem (7) (consumidor)
def clone_callback(ch, method, properties, body):
    body = body.decode('utf-8')
    if 'user' in body:
        try:
            str_temp = body.split(',')
            user = str_temp[0].split('=')[1]
            repositorio = str_temp[1].split('=')[1]
            print(f'Faz a clonagem do {repositorio}, na area do usuario: {user}')
            git_url = repositorio        
            separa_ponto = git_url.split('.')
            nome_repositorio_temp = separa_ponto[1]
            nome_repositorio = nome_repositorio_temp.split('/')[-1]
            repo_dir = nome_repositorio
            if not os.path.isdir(repo_dir):
                try:
                    Repo.clone_from(git_url, repo_dir)
                    print(f'Repositório {git_url} clonado com sucesso!')
                    # 3.1. Dispara uma solicitação para atualizar o status do repositório no BD (9)
                    msg_update_db_repositorio(canal=channel_to_update_db, fila=my_fila2, usuario=user, repositorio=repositorio)
                except Exception as ex:
                    print(f'Erro: {str(ex)}')
            else:
                print(f'O repositório {git_url} já foi clonado no diretório {repo_dir}')
        except Exception as ex:
            print(f'Erro: {str(ex)}')     
 
channel_to_clone.basic_consume(my_fila1, clone_callback, auto_ack=True)
 
print(' [*] Waiting for messages to cloning. To exit press CTRL+C')
channel_to_clone.start_consuming()