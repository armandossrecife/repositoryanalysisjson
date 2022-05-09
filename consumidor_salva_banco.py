# Consumidor e Produtor
# Consumidor da fila 'fila_banco'
# Produtor na fila 'fila_repositorio_local'

import pika
from git import Repo
import os
import utils as util
 
rabbitmq_broker_host = 'localhost'
my_fila1 = 'fila_banco'
my_fila2 = 'fila_repositorio_local'
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_broker_host))

channel_salva_banco = connection.channel()
channel_salva_banco.queue_declare(queue=my_fila1, durable=True)

channel_to_clone = connection.channel() 
channel_to_clone.queue_declare(queue=my_fila2, durable=True)

# 1.3. Consome da fila de operações do BD (3) (consumidor)
def salva_no_banco_callback(ch, method, properties, body):
    body = body.decode('utf-8')
    if 'user' in body:
        try:
            user, repositorio, nome_repositorio, status = util.parser_body(body)
            if not os.path.isdir(nome_repositorio):
                try:
                    # 1.4. Repositório salvo no BD (4)
                    util.salvar_no_banco(user, repositorio, nome_repositorio, status)
                    # 2.1. Dispara uma solicitação para clonar o repositório no sistema de arquivo local (5)
                    msg_clona_repositorio(canal=channel_to_clone, fila=my_fila2, usuario=user, repositorio=repositorio, status='Clonado')
                except Exception as ex:
                    print(f'Erro: {str(ex)}')
            else:
                print(f'O repositório {repositorio} já foi clonado no diretório {nome_repositorio}')
        except Exception as ex:
            print(f'Erro: {str(ex)}')     

# 2.2. Enfilera pedido de clonagem do repositório (6) (produtor)
def msg_clona_repositorio(canal=channel_to_clone, fila=my_fila2, usuario='', repositorio='', status=''):
    print(f'Conectando ao canal channel_to_clone na fila {fila}')
    print(f'Enviando o pedido de clonagem do repositório {repositorio} do usuário {usuario}')
    conteudo = 'user=' + usuario + ',' + 'repository=' + repositorio + ',' + 'status='+status
    canal.basic_publish(exchange='', routing_key=fila, body=conteudo)
 
channel_salva_banco.basic_consume(my_fila1, salva_no_banco_callback, auto_ack=True)
 
print(' [*] Waiting for messages to save repository in BD. To exit press CTRL+C')
channel_salva_banco.start_consuming()