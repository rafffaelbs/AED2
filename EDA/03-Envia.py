from neo4j import GraphDatabase
import time
import math

# URI e credenciais de conexão para o banco de dados Neo4j
URI = "neo4j+ssc://e0e98921.databases.neo4j.io"     
USERNAME = "neo4j"
PASSWORD = "giqAxWG-g-MYyLiykQZ7gU1JUS7E16PcT3Vw_ZyNNt0"
AUTH = ("neo4j", "giqAxWG-g-MYyLiykQZ7gU1JUS7E16PcT3Vw_ZyNNt0")

# Função para conectar ao Neo4j e executar uma query Cypher
def conecta_neo4j(query):
    # Estabelecer conexão com o banco de dados
    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
    with driver.session() as session:
        # Executar a query
        result = session.run(query)
        # Consumir todos os registros do resultado
        records = list(result)
        return records
    # Fechar o driver após o uso
    driver.close()

# Verificar conectividade com o banco de dados
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

# Lista de comandos Cypher para criar restrições (constraints) no banco de dados
a = [
    "CREATE CONSTRAINT unique_movie_title_year IF NOT EXISTS FOR (m:Movie) REQUIRE (m.title, m.year) IS UNIQUE",
    "CREATE CONSTRAINT director_name IF NOT EXISTS FOR (d:Director) REQUIRE d.name IS UNIQUE",
    "CREATE CONSTRAINT actor_name IF NOT EXISTS FOR (a:Actor) REQUIRE a.name IS UNIQUE",
    "CREATE CONSTRAINT genre_name IF NOT EXISTS FOR (g:Genre) REQUIRE g.name IS UNIQUE",
    "CREATE CONSTRAINT user_name IF NOT EXISTS FOR (u:User) REQUIRE u.name IS UNIQUE"
]

# Executar cada comando Cypher para criar as restrições
for x in range(len(a)):
    conecta_neo4j(a[x])
print("Nós Criados [Teoricamente]")

# Lista de arquivos que contêm comandos Cypher para criação de nós e relacionamentos
cria = ["neo4j_diretor.txt","neo4j_filme.txt", "neo4j_genero.txt","neo4j_ator.txt", "neo4j_relacionamentos.txt"]

# Processar cada arquivo da lista
for x in range(len(cria)):
    print(f"Abrindo {cria[x]}: \n")
    with open(cria[x], 'r') as file:
        texto = file.readlines()
    
    tamanho = len(texto)
    texto_formatado = ('').join(texto)
    
    # Calcular quantas partes de 200 linhas são necessárias
    resto = tamanho % 200
    rang = math.ceil(tamanho / 200)

    # Processar arquivos que não são "neo4j_relacionamentos.txt"
    if cria[x] != "neo4j_relacionamentos.txt":
        for z in range(rang):
            a = ''
            if (z != rang - 1) or (resto == 0):
                a += ('').join(texto[(z * 200):((z + 1) * 200)])
                a += '\n\n'
            else:
                a += ('').join(texto[(z * 200):((z * 200) + resto)])

            conecta_neo4j(a)
            print(f'Teoricamente Enviado.')

    # Processar "neo4j_relacionamentos.txt" separando comandos Cypher por "\n\n"
    else:
        z = 1
        consultas = texto_formatado.split('\n\n')
        for y in range(len(consultas)):
            conecta_neo4j(consultas[y])
        z += 1
