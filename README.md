# repositoryanalysis
Repository Analysis - Permite a análise assíncrona de vários repositórios git de forma "simultânea"

Dado um repositório git o mesmo é salvo em banco e logo depois é clonado para permitir uma análise local. Ao final da análise do repositório gera um arquivo JSON com os resultados da análise.

## Para rodar o RabbitMQ com o docker, basta rodar a seguinte linha de comando:
```
$ docker run --rm -p 5672:5672 -p 8080:15672 rabbitmq:3-management
```

O servidor de mensageria do RabbitMQ deverá rodar em http://localhost:8080

Entre com o usuário guest/guest

Crie as seguintes filas: 

fila_banco - Fila que organiza as solicitações para salvar as informações dos repositórios no banco

fila_repositorio_local - Fila que organiza as solicitações para clonar os repositórios

fila_analise_commits - Fila que organiza as solicitações de análise dos repositórios

fila_operacoes_arquivo_local - Fila que organiza a geração de arquivos JSON contendo os resultados das análises de cada repositório

fila_status_banco - Fila que organiza as solicitações de atualização de status de cada repositório no banco

### Para visualizar as mensagens de uma fila no RabbitMQ:
```
$ rabbitmqadmin get queue=fila_operacoes_arquivos_local count=10
```

## Executando os produtores e consumidores

Dispara mensgem para a fila_banco (pedido para salvar o repositório no BD)
```
# Shell 1
$ python3 produtor_salva_banco.py
```

Consumidor da fila_banco e produtor da fila_repositorio_local - atualiza no banco e solicta clonagem - (consumidor e produtor)
```
# Shell 2
$ python3 consumidor_salva_banco.py 
```

Consumidor da fila_repositorio_local e produtor da fila_status_banco - faz a clonagem e solicita atualização do BD - (consumidor e produtor)
```
# Shell 3
$ python3 consumidor_clona_repositorio.py
```

Consumidor da fila_status_banco e produtor da fila_analise_commits - atualiza o BD e solicita análise do repositório - (consumidor e produtor)
```
# Shell 4
$ python3 consumidor_atualiza_status_banco.py
```

Consumidor da fila_analise_commits e produtor da fila_operacoes_arquivos_local - analisa os commits do repositório e solicita gerar JSON - (consumidor e produtor)
```
# Shell 5
$ python3 consumidor_analisa_commits.py
```

Consumidor da fila_arquivos_local - Gera o arquivo JSON com os resultados da análise do repositório.
```
# Shell 6
$ python3 consumidor_gera_json.py 
```
