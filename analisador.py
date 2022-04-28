import pika
from tqdm import tqdm
import time
 
rabbitmq_broker_host = 'localhost'
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_broker_host))

channel_to_analysis = connection.channel() 
channel_to_analysis.queue_declare(queue='analysis', durable=True)

channel_to_update_db = connection.channel() 
channel_to_update_db.queue_declare(queue='updatedb', durable=True)

def msg_updatedb_repositorio(canal=channel_to_update_db, fila='updatedb', usuario='', repositorio=''):
    print(f'Conectando ao canal channel_to_update_db na fila {fila}')
    print(f'Enviando o pedido de atualizacao do repositório {repositorio} no banco')
    conteudo = 'user=' + usuario + ',' + 'repository=' + repositorio
    canal.basic_publish(exchange='', routing_key=fila, body=conteudo)

def analise_callback(ch, method, properties, body):
    body = body.decode('utf-8')
    if 'user' in body:
        try:
            str_temp = body.split(',')
            user = str_temp[0].split('=')[1]
            repositorio = str_temp[1].split('=')[1]
            print(f'Faz a analise do {repositorio}, na area do usuario: {user}')            
            for i in tqdm(range(5)):
                time.sleep(1)
            print(f'Análise do repositório {repositorio} concluida!')
            msg_updatedb_repositorio(canal=channel_to_update_db, fila='updatedb', usuario=user, repositorio=repositorio)
        except Exception as ex:
            print(f'Erro: {str(ex)}')     
 
channel_to_analysis.basic_consume('analysis', analise_callback, auto_ack=True)
 
print(' [*] Waiting for messages to analysis queue. To exit press CTRL+C')
channel_to_analysis.start_consuming()