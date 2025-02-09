# Consumidor e Produtor
# Consumidor da fila 'fila_repositorio_local'
# Produtor na fila 'fila_status_banco'

import pika
from git import Repo
import os
import utils as util
 
rabbitmq_broker_host = 'localhost'
my_fila1 = 'fila_repositorio_local'
my_fila2 = 'fila_status_banco'

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_broker_host))

channel_to_clone = connection.channel()
channel_to_clone.queue_declare(queue=my_fila1, durable=True)

channel_to_update_db = connection.channel() 
channel_to_update_db.queue_declare(queue=my_fila2, durable=True)

# 2.3. Consome da fila de operações de clonagem (7) (consumidor)
def clone_callback(ch, method, properties, body):
    body = body.decode('utf-8')
    if 'user' in body:
        try:
            user, repositorio, nome_repositorio, status = util.parser_body(body)
            print(f'Faz a clonagem do {repositorio}, na area do usuario: {user}')       
            if not os.path.isdir(nome_repositorio):
                try:
                    Repo.clone_from(repositorio, nome_repositorio)
                    print(f'Repositório {repositorio} clonado com sucesso!')
                    # 3.1. Dispara uma solicitação para atualizar o status do repositório no BD (9)
                    msg_update_db_repositorio(canal=channel_to_update_db, fila=my_fila2, usuario=user, repositorio=repositorio, status='Clonado')
                except Exception as ex:
                    print(f'Erro: {str(ex)}')
            else:
                print(f'O repositório {repositorio} já foi clonado no diretório {nome_repositorio}')
        except Exception as ex:
            print(f'Erro: {str(ex)}')     

# 3.2. Enfilera pedido de atualização do status do repositório no BD (10) (produtor)
def msg_update_db_repositorio(canal=channel_to_update_db, fila=my_fila2, usuario='', repositorio='', status=''):
    print(f'Conectando ao canal channel_to_update_db na fila {fila}')
    print(f'Enviando o pedido de update do repositório {repositorio} no BD')
    conteudo = 'user=' + usuario + ',' + 'repository=' + repositorio + ',' + 'status='+status
    canal.basic_publish(exchange='', routing_key=fila, body=conteudo)
 
channel_to_clone.basic_consume(my_fila1, clone_callback, auto_ack=True)
 
print(' [*] Waiting for messages to cloning. To exit press CTRL+C')
channel_to_clone.start_consuming()