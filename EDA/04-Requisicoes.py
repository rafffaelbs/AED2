from neo4j import GraphDatabase
import pandas as pd

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j+ssc://e0e98921.databases.neo4j.io"  # Conexão com o banco de dados Neo4j
USERNAME = "neo4j"
PASSWORD = "giqAxWG-g-MYyLiykQZ7gU1JUS7E16PcT3Vw_ZyNNt0"
AUTH = (USERNAME, PASSWORD)

# Carregar a lista de filmes a partir de um arquivo CSV e formatar os títulos
filmografia = pd.read_csv('filmes.csv')
filmografia = filmografia['Title'].tolist()
filmografia = list(map(str.title, filmografia))

def execute_cypher_query(uri, username, password, query):
    # Função para executar uma consulta Cypher no banco de dados Neo4j
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        result = session.run(query)
        records = list(result)  # Consumir todos os registros
        return records
    driver.close()  # Fechar o driver

def enviar(texto):
    # Função para enviar uma consulta Cypher e retornar os resultados
    cypher_query = texto
    records = execute_cypher_query(URI, USERNAME, PASSWORD, cypher_query)
    return records

def verifica_usuario(usuario):
    # Verificar se um usuário existe no banco de dados
    query = f"MATCH (n:User {{nome: '{usuario}'}}) Return n"
    records = execute_cypher_query(URI, USERNAME, PASSWORD, query)
    if len(records) != 0:
        return 1
    else:
        return 0

def adicionar_usuario(usuario):
    # Adicionar um novo usuário se ele não existir no banco de dados
    ver = verifica_usuario(usuario)
    if ver == 0:
        query = f"MERGE ({usuario}:User {{nome:'{usuario}'}})"
        enviar(query)
        print("Usuario Adicionado")
    else:
        print("Este usuário já foi adicionado")

def adicionar_filmes(usuario, filmes):
    # Adicionar filmes que um usuário assistiu
    ver = verifica_usuario(usuario)
    if ver == 0:
        print("Usuário não encontrado. Tente Novamente")
        return 
    cont2 = 0 
    query = ""
    for filme in filmes:
        query += f"MATCH (filme{cont2}:Movie {{title:'{filme}'}}) "
        cont2 += 1
    cont2 = 0
    for filme in filmes:
        query += f"MERGE (user:User {{nome:'{usuario}'}})-[:ASSISTIU]->(filme{cont2}) "
        cont2 += 1
    enviar(query)

def recomendacao(usuario):
    # Obter recomendações de filmes para um usuário com base em seus filmes assistidos
    ver = verifica_usuario(usuario)
    if ver == 0:
        print("Usuário não encontrado. Tente Novamente")
        return 
    query = f"""
        MATCH (usuario:User {{nome: '{usuario}'}})-[:ASSISTIU]->(filme:Movie)
        WITH filme, usuario
        MATCH (filme)-[:ATUA_EM|DIRIGE|TEM_GENERO]-(relacionado)
        MATCH (relacionado)-[:ATUA_EM|DIRIGE|TEM_GENERO]-(recomendacao:Movie)
        WHERE NOT (usuario)-[:ASSISTIU]->(recomendacao)
        WITH recomendacao, COUNT(*) as score
        ORDER BY score DESC
        LIMIT 10
        MATCH (recomendacao)-[:DIRIGE]->(d:Director)
        MATCH (recomendacao)-[:TEM_GENERO]->(g:Genre)
        RETURN recomendacao, score, COLLECT(DISTINCT d.name) as diretores, COLLECT(DISTINCT g.name) as generos
    """
    records = enviar(query)

    # Exibir recomendações
    print('Aqui estão alguns filmes que você pode gostar:')
    cont = 0
    print(f"\t Pos | {'Filme':^30} - {'Diretor':^30} - {'Ano':^10} - {'Genero Principal':^15} - {'Nota':^15} - {'Proximidade':^15}")
    for record in records:
        print(f"\t {cont+1:^2}º | {record['recomendacao']['title']:^30} - {record['diretores'][0]:^30} - {record['recomendacao']['year']:^10} - {record['generos'][0]:^15} - {record['recomendacao']['rating']:^15} - {record['score']:^15}")
        cont += 1

while True:
    # Menu de operações
    a = int(input(f"""{"-"*70}
            \t[1] - Adicionar novo usuário
            \t[2] - Adicionar filmes
            \t[3] - Ver Recomendação
            \t[4] - Fazer Consulta Cypher Personalizada 
            \t[5] - Encerrar\n{"-"*70}\nInsira o número da operação que você deseja realizar: \033[32m"""))
    print("\033[m")
    if a == 1: 
        usuario = input("Adicione o nome do novo usuário: ")
        adicionado = adicionar_usuario(usuario)    
    
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
        query = input("Insira sua requisição Cypher: ")
        print(enviar(query))
    
    if a == 5:
        break
