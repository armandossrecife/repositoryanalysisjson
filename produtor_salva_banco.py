# Produtor da fila 'fila_banco'
import pika
   
rabbitmq_host = 'localhost'
my_fila = 'fila_banco'
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel_salva_banco = connection.channel() 
channel_salva_banco.queue_declare(queue=my_fila, durable=True)

# 1.2. Enfilera solicitação na fila (2) (produtor) (ok)  
def msg_salva_repositorio_no_banco(fila=my_fila, usuario='', repositorio='', status=''):
    print(f'Conectando ao canal channel_salva_banco na fila {fila}')
    print(f'O {usuario} dispara uma solicitação para salvar o repositório {repositorio} no BD')
    conteudo = 'user=' + usuario + ',' + 'repository=' + repositorio + ',' + 'status=' + status
    print(f'body={conteudo}')
    channel_salva_banco.basic_publish(exchange='', routing_key=fila, body=conteudo)
    print(f'Enviado o pedido para salvar o repositório {repositorio} no BD para o usuário {usuario}')

# Exemplos
# 1.1. Dispara uma solicitação para salvar o repositório no BD (1) (ok)
msg_salva_repositorio_no_banco(fila=my_fila, usuario='armando', repositorio='https://github.com/myplayareas/rabbitmq.git', status='Registrado')

# 1.1. Dispara uma solicitação para salvar o repositório no BD (1) (ok)
msg_salva_repositorio_no_banco(fila=my_fila, usuario='armando', repositorio='https://github.com/myplayareas/sysrepository.git', status='Registrado')

# 1.1. Dispara uma solicitação para salvar o repositório no BD (1) (ok)
msg_salva_repositorio_no_banco(fila=my_fila, usuario='armando', repositorio='https://github.com/myplayareas/treemap.git', status='Registrado')

connection.close()