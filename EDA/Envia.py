from py2neo import Graph

# Conectar ao Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "B8kCtcJ-uCoEelQKCdlYlMxCnol07758SF0ZfimNF-E"))

path = "C:/Users/rafae/Code/Outros/Python/Projetos/Neo4j/neo4j_relacionamentos.txt"
with open(path, 'r') as file:
    texto = file.readlines()

texto = ('').join(texto)

#print(type(texto))
consultas = texto.split('\n\n')

for i in range(len(consultas)):    
    query = consultas[i]
    result = graph.run(query)
