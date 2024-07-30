from neo4j import GraphDatabase
import pandas as pd
import os

# Configurações de conexão com o banco de dados Neo4j
URI = "neo4j+ssc://e0e98921.databases.neo4j.io" # Endereço do banco de dados
USERNAME = "neo4j" # Nome de usuário do Neo4j
PASSWORD = "giqAxWG-g-MYyLiykQZ7gU1JUS7E16PcT3Vw_ZyNNt0" # Senha do Neo4j

# Leitura do arquivo CSV e formatação dos títulos dos filmes
filmografia = pd.read_csv('filmes.csv')
filmografia = filmografia['Title'].tolist()
filmografia = list(map(str.title, filmografia))

# Função para limpar o terminal no Windows
def clear_terminal():
    os.system('cls')

# Função para executar consultas Cypher no banco de dados Neo4j
def execute_cypher_query(uri, username, password, query):
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        result = session.run(query)
        records = list(result)  # Consumir todos os registros
        return records
    driver.close()  # Fechar o driver

# Função auxiliar para enviar uma consulta Cypher e obter os resultados
def enviar(texto):
    cypher_query = texto
    records = execute_cypher_query(URI, USERNAME, PASSWORD, cypher_query)
    return records

# Função para verificar se um usuário já existe no banco de dados
def verifica_usuario(usuario):
    query = f"MATCH (n:User {{nome: '{usuario}'}}) Return n"
    records = execute_cypher_query(URI, USERNAME, PASSWORD, query)
    if len(records) != 0:
        return 1
    else:
        return 0

# Função para adicionar um novo usuário ao banco de dados
def adicionar_usuario(usuario):
    ver = verifica_usuario(usuario)
    if ver == 0:
        query = f"MERGE ({usuario}:User {{nome:'{usuario}'}})"
        enviar(query)
        print("Usuario Adicionado")
    else:
        print("Este usuário já foi adicionado")

# Função para adicionar filmes assistidos por um usuário
def adicionar_filmes(usuario, filmes):
    ver = verifica_usuario(usuario)
    if ver == 0:
        print("Usuário não encontrado. Tente Novamente")
        return 
    cont2 = 0 
    query = f"MATCH (user:User {{nome:'{usuario}'}})"
    for filme in filmes:
        query += f"MATCH (filme{cont2}:Movie {{title:'{filme}'}})"
        cont2 += 1
    cont2 = 0
    for filme in filmes:
        query += f"MERGE (user)-[:ASSISTIU]->(filme{cont2})"
        cont2 += 1
    enviar(query)
    print("Filmes adicionados com sucesso")

# Função para recomendar filmes a um usuário
def recomendacao(usuario):
    ver = verifica_usuario(usuario)
    if ver == 0:
        print("Usuário não encontrado. Tente Novamente")
        return 
    query = f"""
        MATCH (usuario:User {{nome: '{usuario}'}})-[:ASSISTIU]->(filme:Movie)
        WITH filme, usuario
        MATCH (filme)-[:ATUA_EM|DIRIGE|TEM_GENERO]-(relacionado)
        MATCH (relacionado)-[:ATUA_EM|DIRIGE|TEM_GENERO]-(recomendacao:Movie)
        MATCH (d:Director)-->(recomendacao)-->(g:Genre)
        WHERE NOT (usuario)-[:ASSISTIU]->(recomendacao)
        RETURN recomendacao, COUNT(*) as score, d.name as diretor, COLLECT (DISTINCT g.name) as genero
        ORDER BY score DESC
        LIMIT 10
        """
    records = enviar(query)    

    print('Aqui estão alguns filmes que você pode gostar:')
    cont = 0
    print(f"\t Pos | {'Filme':^30} - {'Diretor':^30} - {'Ano':^10} - {'Genero Principal':^15} - {'Nota':^15} - {'Proximidade':^15}")
    for record in records:
        if (len(record['recomendacao']['title']) > 25):
            rec = record['recomendacao']['title'][0:25] + "..."
        else:
            rec = record['recomendacao']['title']
        print(f"\t {cont+1:^2}º | {rec:^30} - {record['diretor']:^30} - {record['recomendacao']['year']:^10} - {record['genero'][0]:^15} - {record['recomendacao']['rating']:^15} - {record['score']:^15}")
        cont += 1

# Função para seguir outro usuário
def seguir_usuario():
    query = "MATCH (n:User) Return n.nome as usuar"
    resuls = enviar(query)
    print(f"\n{'-'*70}\n{'Lista de Usuários':^70}\n{'-'*70}")
    cont = 0
    usuarios = []
    for resul in resuls:
        usuarios.append(resul['usuar'])
        print(f"{str([cont+1]):>30} - {resul['usuar']}")
        cont += 1
    print(f"\n{'-'*70}\n")
    usuario = input('Insira seu nome de usuario: ')
    seguir = int(input("Insira o número do usuário que deseja seguir [Ou '0' para continuar]: "))
    if seguir == 0:
        return 0
    seguir = usuarios[seguir-1]
    query = f"""
    MATCH (user:User {{nome: '{usuario}'}})
    MATCH (segue:User {{nome: '{seguir}'}})
    MERGE (user)-[:SEGUE]->(segue)
    """
    enviar(query)
    print(f"{usuario} seguindo o usuário {seguir} com Sucesso !\n{'-'*70}\n")

# Função para exibir estatísticas de um usuário
def estatistica_usuario(usuario):
    query = f"MATCH (user:User {{nome: '{usuario}'}})-[r:ASSISTIU]-(m:Movie) Return count(*) as Qntd"
    resul = enviar(query)
    print(f"{'-'*70}\n\033[34mQuantidade de filmes assistidos pelo usuário\033[m {usuario}\033[34m : {resul[0]['Qntd']}")

    query = f"MATCH (user:User {{nome: '{usuario}'}})--(m:Movie) MATCH (d:Director)--(m) RETURN DISTINCT d.name as Diretor, count(*) as Qntd ORDER BY Qntd DESC LIMIT 5"
    print(f"{'-'*70}\n\033[34mTop 5 Diretores Mais Assistidos: \033[m")
    results = enviar(query)
    cont = 1
    for resul in results:
        print(f"\t\t{cont}º - {resul['Diretor']} - {resul['Qntd']} Aparições")
        cont += 1
    
    print(f"{'-'*70}\n\033[34mTop 5 Atores Mais Assistidos: \033[m")
    query = f"MATCH (user:User {{nome: '{usuario}'}})--(m:Movie) MATCH (a:Actor)--(m) RETURN DISTINCT a.name as Ator, count(*) as Qntd ORDER BY Qntd DESC LIMIT 5"  
    results = enviar(query)
    cont = 1
    for resul in results:
        print(f"\t\t{cont}º - {resul['Ator']} - {resul['Qntd']} Aparições")
        cont += 1
    
    print(f"{'-'*70}\n\033[34mTop 5 Generos Mais Assistidos: \033[m")
    query = f"MATCH (user:User {{nome: '{usuario}'}})--(m:Movie) MATCH (g:Genre)--(m) RETURN DISTINCT g.name as Genero, count(*) as Qntd ORDER BY Qntd DESC LIMIT 5"
    results = enviar(query)
    cont = 1
    for resul in results:
        print(f"\t\t{cont}º - {resul['Genero']} - {resul['Qntd']} Aparições")
        cont += 1

    print(f"{'-'*70}")

# Loop principal para interagir com o usuário
while True:
    a = int(input(f"""{"-"*70}
            \t[1] - Adicionar novo usuário
            \t[2] - Adicionar filmes
            \t[3] - Ver Recomendação
            \t[4] - Seguir Usuários 
            \t[5] - Visualizar Estatisticas de Usuário
            \t[6] - Fazer Consulta Cypher Personalizada
            \t[7] - Encerrar\n{"-"*70}\nInsira o número da operação que você deseja realizar: \033[32m"""))
    print("\033[m")
    if a == 1: 
        usuario = input("Adicione o nome do novo usuário: ")
        adicionar_usuario(usuario)    
    
    if a == 2:
        usuario = input("Insira seu nome de usuário: ")
        quantidade = int(input("Numero de filmes que deseja adicionar: "))
        filmes = []
        cont = 0
        print(f'Adicionando filmes para o usuário {usuario}')
        while True:
            a = (input(f"\tAdicione nome do {cont+1}º filme (Título no Idioma Original / Romanizado): ")).title()
            if a not in filmografia:
                print(f'\tFilme não Encontrado.\n\tSe a ortografia estiver correta, é provavél que esse filme não se encontra no Top 1000 IMDB\n\tPor favor, tente novamente\n')
            else: 
                filmes.append(a)
                cont += 1
            if cont >= quantidade:
                break
        adicionar_filmes(usuario, filmes)
        
    if a == 3:
        usuario = input("Para qual usuario voce deseja ver a recomendação ? ")
        recomendacao(usuario)

    if a == 4:
        seguir_usuario()

    if a == 5:
        usuario = input("Insira seu nome de usuário: ")
        estatistica_usuario(usuario)

    if a == 6:
        query = input("Insira sua requisição Cypher: ")
        resuls= (enviar(query))
        for resul in resuls:
            print (resul)

    if a == 7:
        break

    a = input('\033[30m Pressione Qualquer Tecla Para Continuar: \033[m')
    clear_terminal()
