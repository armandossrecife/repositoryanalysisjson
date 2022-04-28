import pika
from git import Repo
import os
 
rabbitmq_broker_host = 'localhost'
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_broker_host))

channel_to_clone = connection.channel()
channel_to_clone.queue_declare(queue='cloning', durable=True)

channel_to_analysis = connection.channel() 
channel_to_analysis.queue_declare(queue='analysis', durable=True)

def msg_analise_repositorio(canal=channel_to_analysis, fila='analysis', usuario='', repositorio=''):
    print(f'Conectando ao canal channel_to_analysis na fila {fila}')
    print(f'Enviando o pedido de analise do repositório {repositorio}')
    conteudo = 'user=' + usuario + ',' + 'repository=' + repositorio
    canal.basic_publish(exchange='', routing_key=fila, body=conteudo)

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
                    msg_analise_repositorio(canal=channel_to_analysis, fila='analysis', usuario=user, repositorio=repositorio)
                except Exception as ex:
                    print(f'Erro: {str(ex)}')
            else:
                print(f'O repositório {git_url} já foi clonado no diretório {repo_dir}')
        except Exception as ex:
            print(f'Erro: {str(ex)}')     
 
channel_to_clone.basic_consume('cloning', clone_callback, auto_ack=True)
 
print(' [*] Waiting for messages to cloning. To exit press CTRL+C')
channel_to_clone.start_consuming()