# 3. Operação de atualizar Banco de Dados 
# produtor_atualiza_status_banco
# fila_status_banco
# consumidor_atualiza_status_banco

# 3.1. Dispara uma solicitação para atualizar o status do repositório no BD (9)
# 3.2. Enfilera pedido de atualização do status do repositório no BD (10) (produtor)
# 3.3. Consome da fila de status do BD (11) (consumidor)
# 3.4. Repositório com status atualizado para clonado no BD (12)

import pika
 
rabbitmq_broker_host = 'localhost'
my_fila1 = 'fila_status_banco'
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_broker_host))

channel_to_update_db = connection.channel() 
channel_to_update_db.queue_declare(queue=my_fila1, durable=True)

def update_db_callback(ch, method, properties, body):
    body = body.decode('utf-8')
    if 'user' in body:
        try:
            str_temp = body.split(',')
            user = str_temp[0].split('=')[1]
            repositorio = str_temp[1].split('=')[1]
            print(f'Atualiza o {repositorio} no banco na area do usuario: {user}')
            git_url = repositorio        
            separa_ponto = git_url.split('.')
            nome_repositorio_temp = separa_ponto[1]
            nome_repositorio = nome_repositorio_temp.split('/')[-1]
            repo_dir = nome_repositorio
            print(f'Repositório do {repo_dir} atualizado no banco com sucesso!')
        except Exception as ex:
            print(f'Erro: {str(ex)}')     
 
channel_to_update_db.basic_consume(my_fila1, update_db_callback, auto_ack=True)
 
print(' [*] Waiting for messages to update in DB. To exit press CTRL+C')
channel_to_update_db.start_consuming()
