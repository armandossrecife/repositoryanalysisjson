# 4. Operações de Análises dos Commits
# produtor_analisa_commits
# fila_analisa_commits
# consumidor_analisa_commits

# 4.1. Dispara uma solicitação para analisar os commits do repositório (13)
# 4.2. Enfilera pedido de análise de commits do repositório (14) (produtor)
# 4.3. Consome da fila de análise de commits (15) (consumidor)
# 4.4. Repositório analisado com sucesso (16)

# 5. Operações de gerar arquivo de JSON
# produtor_gera_json
# fila_operacoes_arquivos_locais
# consumidor_gera_json

# 5.5. Dispara uma solicitação para atualizar o status do repositório no BD (17)
# 5.6. Repositório com status atualizado para analisado (18)
# 5.7. Dispara uma solicitação para gerar o JSON com as respostas da análise do repositório (19) 
# 5.8. Enfilera pedido de gerar arquivo JSON do repositório (20) (produtor)
# 5.9. Consome da fila de operações de Arquivos locais (21) (consumidor)
# 5.10. Arquivo JSON da análise do Repositório gerado com sucesso (22)

import pika
from tqdm import tqdm
import time
 
rabbitmq_broker_host = 'localhost'
my_fila1 = 'fila_analise_commits'
my_fila2 = 'fila_operacoes_arquivos_local'
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_broker_host))

channel_to_analysis = connection.channel() 
channel_to_analysis.queue_declare(queue=my_fila1, durable=True)

channel_to_generate_file = connection.channel()
channel_to_generate_file.queue_declare(queue=my_fila2, durable=True)

# 5.7. Dispara uma solicitação para gerar o JSON com as respostas da análise do repositório (19)
def msg_generate_file_repositorio(canal=channel_to_generate_file, fila=my_fila2, usuario='', repositorio=''):
    print(f'Conectando ao canal channel_to_generate_file na fila {fila}')
    print(f'Enviando o pedido de gerar arquivos JSON do repositório {repositorio}')
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
            # 5.8. Enfilera pedido de gerar arquivo JSON do repositório (20) (produtor)
            msg_generate_file_repositorio(canal=channel_to_generate_file, fila=my_fila2, usuario=user, repositorio=repositorio)
        except Exception as ex:
            print(f'Erro: {str(ex)}')     
 
print(' [*] Waiting for messages to analysis queue. To exit press CTRL+C')

channel_to_analysis.basic_consume(my_fila1, analise_callback, auto_ack=True)
 
channel_to_analysis.start_consuming()