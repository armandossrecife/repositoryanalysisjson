from tqdm import tqdm
import time

def salvar_no_banco(usuario, repositorio, nome_repositorio, status):
    print(f'Operação de salvar o {repositorio} no Banco do usuário {usuario}')
    print(f'Repositório {nome_repositorio} salvo no BD com status {status} com sucesso!')

def atualizar_status_no_banco(user, repositorio, status):
    print(f'Atualiza o status {status} do {repositorio} no banco na area do usuario: {user}')

def analisar_repositorio(user, repositorio):
    print(f'Faz a analise do {repositorio}, na area do usuario: {user}')
    for i in tqdm(range(5)):
        time.sleep(1)

def gerar_arquivos_json(user, repositorio):
    try:
        for i in tqdm(range(3)):
            time.sleep(1)
        print(f'Arquivo JSON Repositório {repositorio} gerado com sucesso na área do usuário: {user}!')
    except Exception as ex:
        print(f'Erro: {str(ex)}')

def parser_body(body):
    str_temp = body.split(',')
    user = str_temp[0].split('=')[1]
    repositorio = str_temp[1].split('=')[1] 
    status = str_temp[2].split('=')[1]      
    separa_ponto = repositorio.split('.')
    nome_repositorio_temp = separa_ponto[1]
    nome_repositorio = nome_repositorio_temp.split('/')[-1]
    return user, repositorio, nome_repositorio, status