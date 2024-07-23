import pandas as pd
from unidecode import unidecode

filmes = []
diretores = []
atores = []
generos = []

df = pd.read_csv('C:/Users/rafae/Code/Outros/Python/Projetos/Neo4j/imdb.csv')
#print(df)

def classifica(classificacao):
    if classificacao == 'A':
        return '18'
    elif classificacao == 'UA':
        return '12'
    elif classificacao == 'U':
        return 'L'
    elif classificacao == 'PG-13':
        return '13'
    elif classificacao == 'R':
        return '16'
    elif classificacao == 'PG':
        return '10'
    elif classificacao == 'G':
        return 'L'
    elif classificacao == 'Passed':
        return 'L'
    elif classificacao == 'TV-14':
        return '16'
    elif classificacao == '16':
        return '16'
    elif classificacao == 'TV-MA':
        return '16'    
    elif classificacao == 'Unrated':
        return 'Unrated'
    elif classificacao == 'GP':
        return 'L'
    elif classificacao == 'Approved':
        return 'L'
    elif classificacao == 'TV_PG':
        return '10'
    elif classificacao == 'U/A':
        return '10'
    else:
        return 'Unrated'

def verifica_ator(atores, ator1, ator2, ator3, ator4): 
    ator1 = unidecode(ator1).replace("'", '')
    ator2 = unidecode(ator2).replace("'", '')
    ator3 = unidecode(ator3).replace("'", '')
    ator4 = unidecode(ator4).replace("'", '')
    if ator1 not in atores:
        atores.append(ator1)
    if ator2 not in atores:
        atores.append(ator2)
    if ator3 not in atores:
        atores.append(ator3)
    if ator4 not in atores:
        atores.append(ator4)

def verifica_diretor(diretores, dir): 
    dir = unidecode(dir).replace("'",'')
    if dir not in diretores:
        diretores.append(dir)

def verifica_filme(filmes, filme, ano, rating, classificacao): 
    filme = unidecode(filme)
    filme = filme.replace("'", "").replace('"', '')
    b =classifica(classificacao)
    if filme[0].isnumeric() == True:
        a = 'The'+filme+'_'+ano+'_'+f"{rating}"+'_'+b
    else:
        a = filme+'_'+ano+'_'+f"{rating}"+'_'+b
    if a not in filmes:
        filmes.append(a)

def verifica_genero(generos, genres):
    genres = genres.split(',')
    for genre in genres:     
        genre = unidecode(genre.strip())
        if genre not in generos:
            generos.append(genre)

cont = 0        
for indice, linha in df.iterrows():
    verifica_filme(filmes, linha['Title'], linha['Released_Year'], linha['IMDB_Rating'], linha['Certificate'])
    verifica_diretor(diretores, linha['Director'])
    verifica_ator(atores, linha['Star1'], linha['Star2'], linha['Star3'], linha['Star4'])
    verifica_genero(generos, linha['Genre'])
    #x = input("Continuar: ")
    cont += 1
    if cont >= 150:
        break

for i in range (len(filmes)):
    filmes[i] = filmes[i].split("_")

df_filme = pd.DataFrame(filmes, columns=['Title', 'Released_Year', 'Rating', 'Certificate'])
df_diretor = pd.DataFrame(diretores, columns=['Nome'])
df_ator = pd.DataFrame(atores, columns=['Nome'])
df_genero = pd.DataFrame(generos, columns=['Genero'])

#print(df_filme.head())
#print(df_diretor.head())
#print(df_ator.head())
#print(df_genero.head())

df_filme.to_csv('filmes.csv', index=False, encoding='utf-8')
df_diretor.to_csv('diretores.csv', index=False, encoding='utf-8')
df_ator.to_csv('atores.csv', index=False, encoding='utf-8')
df_genero.to_csv('generos.csv', index=False, encoding='utf-8')
