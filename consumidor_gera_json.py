# Consumidor da fila 'fila_operacoes_arquivos_local'

import pika
from git import Repo
import os
from tqdm import tqdm
import time
 
rabbitmq_broker_host = 'localhost'
my_fila1 = 'fila_operacoes_arquivos_local'
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_broker_host))

channel_to_generate_file = connection.channel()
channel_to_generate_file.queue_declare(queue=my_fila1, durable=True)

def generate_file_callback(ch, method, properties, body):
    body = body.decode('utf-8')
    if 'user' in body:
        try:
            str_temp = body.split(',')
            user = str_temp[0].split('=')[1]
            repositorio = str_temp[1].split('=')[1]
            print(f'Gerar o arquivo JSON do {repositorio}, na area do usuario: {user}')
            git_url = repositorio        
            separa_ponto = git_url.split('.')
            nome_repositorio_temp = separa_ponto[1]
            nome_repositorio = nome_repositorio_temp.split('/')[-1]
            try:
                for i in tqdm(range(3)):
                    time.sleep(1)
                print(f'Arquivo JSON Repositório {git_url} gerado com sucesso!')
            except Exception as ex:
                print(f'Erro: {str(ex)}')
        except Exception as ex:
            print(f'Erro: {str(ex)}')     
 
channel_to_generate_file.basic_consume(my_fila1, generate_file_callback, auto_ack=True)
 
print(' [*] Waiting for messages to generate JSON file from repository. To exit press CTRL+C')
channel_to_generate_file.start_consuming()