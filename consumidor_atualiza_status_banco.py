# Consumidor e Produtor
# Consumidor da fila 'fila_status_banco'
# Produtor na fila 'fila_analise_commits'

import pika
import utils as util
 
rabbitmq_broker_host = 'localhost'
my_fila1 = 'fila_status_banco'
my_fila2 = 'fila_analise_commits'
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_broker_host))

channel_to_update_db = connection.channel() 
channel_to_update_db.queue_declare(queue=my_fila1, durable=True)

channel_to_analysis = connection.channel()
channel_to_analysis.queue_declare(queue=my_fila2, durable=True)

def update_db_callback(ch, method, properties, body):
    body = body.decode('utf-8')
    if 'user' in body:
        try:
            user, repositorio, nome_repositorio, status = util.parser_body(body)
            util.atualizar_status_no_banco(user, repositorio, status)
            print(f'Repositório do {nome_repositorio} atualizado no banco com sucesso!')
            # 4.2. Enfilera pedido de análise de commits do repositório (14) (produtor)
            msg_analysis_db_repositorio(canal=channel_to_update_db, fila=my_fila2, usuario=user, repositorio=repositorio, status='Em analise')
        except Exception as ex:
            print(f'Erro: {str(ex)}')     

# 4.1. Dispara uma solicitação para analisar os commits do repositório (13)
def msg_analysis_db_repositorio(canal=channel_to_update_db, fila=my_fila2, usuario='', repositorio='', status=''):
    print(f'Conectando ao canal channel_to_analysis na fila {fila}')
    print(f'Enviando o pedido de analysis do repositório {repositorio} no BD')
    conteudo = 'user=' + usuario + ',' + 'repository=' + repositorio + ',' + 'status=' + status
    canal.basic_publish(exchange='', routing_key=fila, body=conteudo)

channel_to_update_db.basic_consume(my_fila1, update_db_callback, auto_ack=True)
 
print(' [*] Waiting for messages to update in DB. To exit press CTRL+C')
channel_to_update_db.start_consuming()