# Produtor da fila 'fila_banco'

# 1. Operacões no Banco de Dados
# produtor_salva_banco
# fila_banco
# consumidor_salva_banco

# 1.1. Dispara uma solicitação para salvar o repositório no BD (1) (ok)
# 1.2. Enfilera solicitação na fila (2) (produtor) (ok)
# 1.3. Consome da fila de operações do BD (3) (consumidor)
# 1.4. Repositório salvo no BD (4)

import pika
   
rabbitmq_host = 'localhost'
my_fila = 'fila_banco'
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel_salva_banco = connection.channel() 
channel_salva_banco.queue_declare(queue=my_fila, durable=True)

# 1.2. Enfilera solicitação na fila (2) (produtor) (ok)  
def msg_salva_repositorio_no_banco(fila=my_fila, usuario='', repositorio=''):
    print(f'Conectando ao canal channel_salva_banco na fila {fila}')
    print(f'Dispara uma solicitação para salvar o repositório {repositorio} no BD')
    conteudo = 'user=' + usuario + ',' + 'repository=' + repositorio
    channel_salva_banco.basic_publish(exchange='', routing_key=fila, body=conteudo)
    print(f'Enviado o pedido para salvar o repositório {repositorio} no BD para o usuário {usuario}')

# Exemplos
# 1.1. Dispara uma solicitação para salvar o repositório no BD (1) (ok)
msg_salva_repositorio_no_banco(fila=my_fila, usuario='armando', repositorio='https://github.com/myplayareas/rabbitmq.git')

# 1.1. Dispara uma solicitação para salvar o repositório no BD (1) (ok)
msg_salva_repositorio_no_banco(fila=my_fila, usuario='armando', repositorio='https://github.com/myplayareas/sysrepository.git')

# 1.1. Dispara uma solicitação para salvar o repositório no BD (1) (ok)
msg_salva_repositorio_no_banco(fila=my_fila, usuario='armando', repositorio='https://github.com/myplayareas/treemap.git')

connection.close()