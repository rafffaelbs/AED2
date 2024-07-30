from neo4j import GraphDatabase
import time
import math

# URI exemplo: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "<uri>"
USERNAME = "neo4j"
PASSWORD = "<password>"
AUTH = (USERNAME, PASSWORD)

def conecta_neo4j(query):
    with open('nome_do_arquivo.txt', 'a') as arquivo:
            arquivo.write('nome_do_arquivo.txt')
    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
    with driver.session() as session:
        result = session.run(query)
        records = list(result)  # Consumir todos os registros
        return records
    driver.close()  # Fechar o driver

# Verificar conectividade
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()


a = ["CREATE CONSTRAINT unique_movie_title_year IF NOT EXISTS FOR (m:Movie) REQUIRE (m.title, m.year) IS UNIQUE",
"CREATE CONSTRAINT director_name IF NOT EXISTS FOR (d:Director) REQUIRE d.name IS UNIQUE",
"CREATE CONSTRAINT actor_name IF NOT EXISTS FOR (a:Actor) REQUIRE a.name IS UNIQUE",
"CREATE CONSTRAINT genre_name IF NOT EXISTS FOR (g:Genre) REQUIRE g.name IS UNIQUE",
"CREATE CONSTRAINT user_name IF NOT EXISTS FOR (u:User) REQUIRE u.name IS UNIQUE"]

for x in range (len(a)):
    conecta_neo4j(a[x])
print("Nós Criados [Teoricamente]")

cria = ["neo4j_diretor.txt","neo4j_filme.txt", "neo4j_genero.txt","neo4j_ator.txt", "neo4j_relacionamentos.txt"]
#cria = ["neo4j_filme.txt", "neo4j_relacionamentos.txt"]

for x in range (len(cria)):
    print(f"Abrindo {cria[x]}: \n")
    with open(cria[x], 'r') as file:
        texto = file.readlines()
    
    tamanho = len(texto)
    texto_formatado = ('').join(texto)
    
    resto = tamanho % 200
    rang = math.ceil(tamanho/200)    

    if cria[x] != "neo4j_relacionamentos.txt":
        for z in range(rang):
            a = ''
            if (z != rang - 1) or (resto == 0):
                a += ('').join(texto[(z*200):((z+1)*200)]    )
                a += '\n\n'
            else:
                a += ('').join(texto[(z*200):((z*200)+resto)])

            conecta_neo4j(a)
            print(f'Teoricamente Enviado [{z+1}/{rang}]')
            #time.sleep(3)

    else:
        z = 1
        consultas = texto_formatado.split('\n\n')


        for y in range(len(consultas)):
            #print(consultas[y])
            #x = input("continuar: ")
            conecta_neo4j(consultas[y])
            #time.sleep(2)
        z += 1
