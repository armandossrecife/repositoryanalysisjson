# Consumidor da fila 'fila_operacoes_arquivos_local'
import pika
import utils as util
 
rabbitmq_broker_host = 'localhost'
my_fila1 = 'fila_operacoes_arquivos_local'
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_broker_host))

channel_to_generate_file = connection.channel()
channel_to_generate_file.queue_declare(queue=my_fila1, durable=True)

def generate_file_callback(ch, method, properties, body):
    body = body.decode('utf-8')
    if 'user' in body:
        try:
            user, repositorio, nome_repositorio, status = util.parser_body(body)
            util.gerar_arquivos_json(user, repositorio)
        except Exception as ex:
            print(f'Erro: {str(ex)}')     
 
channel_to_generate_file.basic_consume(my_fila1, generate_file_callback, auto_ack=True)
 
print(' [*] Waiting for messages to generate JSON file from repository. To exit press CTRL+C')
channel_to_generate_file.start_consuming()