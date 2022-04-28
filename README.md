# repositoryanalysis
Repository Analysis

Dado um repositório git o mesmo é salvo em banco e logo depois é clonado para permitir uma análise local.

# Para rodar o RabbitMQ com o docker, basta rodar a seguinte linha de comando:
$ docker run --rm -p 5672:5672 -p 8080:15672 rabbitmq:3-management

1. Cadastrar repositório (produtor na fila cloning)
2. Fazer a análise dos commits do repositório (clonador consome da fila cloning e produz na fila analysis)
3. Gerar o resultado da análise do repositório (analisador consome da fila analysis e produz na fila updatedb)
4. Salvar o status de análise do repositório no banco (update consome da fila updatedb)
