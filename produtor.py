import pika
   
rabbitmq_host = 'localhost'
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel() 
channel.queue_declare(queue='cloning', durable=True)
  
def msg_clona_repositorio(fila='cloning', usuario='', repositorio=''):
    print(f'Conectando ao canal 1 na fila {fila}')
    print(f'Enviando o pedido de clone do repositório {repositorio}')
    conteudo = 'user=' + usuario + ',' + 'repository=' + repositorio
    channel.basic_publish(exchange='', routing_key=fila, body=conteudo)
    print(f'Enviado o pedido de clonagem do repositorio {repositorio} para o usuário {usuario}')

msg_clona_repositorio(fila='cloning', usuario='armando', repositorio='https://github.com/myplayareas/rabbitmq.git')
msg_clona_repositorio(fila='cloning', usuario='armando', repositorio='https://github.com/myplayareas/sysrepository.git')
msg_clona_repositorio(fila='cloning', usuario='armando', repositorio='https://github.com/myplayareas/treemap.git')

connection.close()