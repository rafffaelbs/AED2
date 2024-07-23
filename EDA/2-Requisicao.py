# Faz as Requisições para a criacao dos nós e relacionamentos
import pandas as pd
from unidecode import unidecode

def cria_arquivo(nome, arq):
    nome_do_arquivo = nome+'.txt'

    # Abrir o arquivo no modo de escrita ('w')
    with open(nome_do_arquivo, 'w') as arquivo:
        # Escrever os dados no arquivo
        arquivo.write(arq)

    print(f"Dados foram escritos no arquivo {nome_do_arquivo} com sucesso.")



filmes = pd.read_csv('C:/Users/rafae/Code/Outros/Python/Projetos/Neo4j/filmes.csv')
generos = pd.read_csv('C:/Users/rafae/Code/Outros/Python/Projetos/Neo4j/generos.csv')
diretores = pd.read_csv('C:/Users/rafae/Code/Outros/Python/Projetos/Neo4j/diretores.csv')
atores = pd.read_csv('C:/Users/rafae/Code/Outros/Python/Projetos/Neo4j/atores.csv')
imdb = pd.read_csv('C:/Users/rafae/Code/Outros/Python/Projetos/Neo4j/imdb.csv')
a = ''

for indice, linha in filmes.iterrows():
    titulo = linha['Title']
    tit = titulo.replace(' ', '').replace(',', '').replace('-', '').replace('.', '').replace('*', '').replace('!', '').replace('?', '').replace('/', '').replace('&', '').replace('(', '').replace(')', '')
    tit = tit.replace(':', '').replace("'", "")

    if tit[0].isnumeric() is True:
        tit = 'The'+tit
    tit = tit + str(linha['Released_Year'])

    a += (f"MERGE ({tit}:Movie {{title:'{titulo}'}}) ON CREATE SET {tit}.year='{linha['Released_Year']}', {tit}.certificate='{linha['Certificate']}', {tit}.rating='{linha['Rating']}'\n")

cria_arquivo('neo4j_filme', a)

a = ''
for indice, linha in generos.iterrows():
    tit = linha['Genero'].replace('-', '')
    a += (f"MERGE ({tit}:Genre {{name:'{tit}'}})\n") 

cria_arquivo('neo4j_genero', a)

a = ''
for indice, linha in atores.iterrows():
    tit = linha['Nome']
    titulo = tit
    tit = tit.replace(' ', '').replace("'","").replace('.', '').replace('-', '')
    a += (f"MERGE ({tit}:Actor {{name:'{titulo}'}})\n") 

cria_arquivo('neo4j_ator', a)

a = ''
for indice, linha in diretores.iterrows():
    tit = linha['Nome']
    titulo = tit
    tit = tit.replace(' ', '').replace("'","").replace('.', '').replace('-', '')
    a += (f"MERGE ({tit}:Director {{name:'{titulo}'}})\n") 

cria_arquivo('neo4j_diretor', a)


cont = 0
cont2 = 0
a = ''

for indice, linha in imdb.iterrows():

    ator1 = unidecode(linha['Star1'].replace("'",""))
    ator2 = unidecode(linha['Star2'].replace("'",""))
    ator3 = unidecode(linha['Star3'].replace("'",""))
    ator4 = unidecode(linha['Star4'].replace("'",""))
    diretor = unidecode(linha['Director'].replace("'",""))
    tit = unidecode(linha['Title']).replace("'", "")
    
    

    a += f"MATCH (movie:Movie {{title: '{tit}'}})\n"    
    a += f"MATCH (actor1:Actor {{name: '{ator1}'}})\n"
    a += f"MATCH (actor2:Actor {{name: '{ator2}'}})\n"
    a += f"MATCH (actor3:Actor {{name: '{ator3}'}})\n"
    a += f"MATCH (actor4:Actor {{name: '{ator4}'}})\n"
    a += f"MATCH (dir:Director {{name: '{diretor}'}})\n"


    generos = linha['Genre'].split(',')
    lista_genero = []
    for genero in generos:
        genero = unidecode(genero.replace('-', '').replace(' ', ''))
        a += f"MATCH (genre{genero}:Genre {{name: '{genero}'}})\n"
        lista_genero.append(genero)
    for i in lista_genero:     
        a += f'MERGE (movie)-[:TEM_GENERO]->(genre{i})\n'


    a += f'MERGE (actor1)-[:ATUA_EM]->(movie)\n'
    a += f'MERGE (actor2)-[:ATUA_EM]->(movie)\n'
    a += f'MERGE (actor3)-[:ATUA_EM]->(movie)\n'
    a += f'MERGE (actor4)-[:ATUA_EM]->(movie)\n'
    a += f'MERGE (dir)-[:DIRIGE]->(movie)\n'
    
    cont += 1
    cont2 += 1
    if cont >= 1:
        a += '\n'
        cont = 0
    #if cont2 >= 10:
     #   break


cria_arquivo('neo4j_relacionamentos', a)
    
