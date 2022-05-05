# Consumidor e Produtor
# Consumidor da fila 'fila_status_banco'
# Produtor na fila 'fila_analise_commits'

import pika
 
rabbitmq_broker_host = 'localhost'
my_fila1 = 'fila_status_banco'
my_fila2 = 'fila_analise_commits'
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_broker_host))

channel_to_update_db = connection.channel() 
channel_to_update_db.queue_declare(queue=my_fila1, durable=True)

channel_to_analysis = connection.channel()
channel_to_analysis.queue_declare(queue=my_fila2, durable=True)

# 4.1. Dispara uma solicitação para analisar os commits do repositório (13)
def msg_analysis_db_repositorio(canal=channel_to_update_db, fila=my_fila2, usuario='', repositorio=''):
    print(f'Conectando ao canal channel_to_analysis na fila {fila}')
    print(f'Enviando o pedido de analysis do repositório {repositorio} no BD')
    conteudo = 'user=' + usuario + ',' + 'repository=' + repositorio
    canal.basic_publish(exchange='', routing_key=fila, body=conteudo)

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
            # 4.2. Enfilera pedido de análise de commits do repositório (14) (produtor)
            msg_analysis_db_repositorio(canal=channel_to_update_db, fila=my_fila2, usuario=user, repositorio=repositorio)
        except Exception as ex:
            print(f'Erro: {str(ex)}')     
 
channel_to_update_db.basic_consume(my_fila1, update_db_callback, auto_ack=True)
 
print(' [*] Waiting for messages to update in DB. To exit press CTRL+C')
channel_to_update_db.start_consuming()