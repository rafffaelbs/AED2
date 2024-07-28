# Recebe csv do IMDB e transforma os dados, pegando as informações relevantes para nosso trabalho e criando novos arquivos, cada um para um tipo de nó que será futuramente criado no NEO4J
import pandas as pd
from unidecode import unidecode

# Listas para armazenar dados extraídos
filmes = []
diretores = []
atores = []
generos = []

# Lê o arquivo CSV dos 1000 filmes mais bem avaliados do IMDB
df = pd.read_csv('arquivos/imdb_top_1000.csv')

# Remove as colunas que não serão utilizadas
df = df.drop(columns=['Gross', 'Runtime', 'No_of_Votes', 'Overview', 'Meta_score', 'Poster_Link'])

# Renomeia a coluna 'Series_Title' para 'Title'
df = df.rename(columns={'Series_Title': 'Title'})

# Função para classificar os filmes de acordo com a classificação indicativa
def classifica(classificacao):
    classificacoes = {
        'A': '18', 'UA': '12', 'U': 'L', 'PG-13': '13', 'R': '16',
        'PG': '10', 'G': 'L', 'Passed': 'L', 'TV-14': '16', '16': '16',
        'TV-MA': '16', 'Unrated': 'Unrated', 'GP': 'L', 'Approved': 'L',
        'TV_PG': '10', 'U/A': '10'
    }
    return classificacoes.get(classificacao, 'Unrated')

# Função para verificar e adicionar atores únicos à lista
def verifica_ator(atores, ator1, ator2, ator3, ator4):
    for ator in [ator1, ator2, ator3, ator4]:
        ator = unidecode(ator).replace("'", '')
        if ator not in atores:
            atores.append(ator)

# Função para verificar e adicionar diretores únicos à lista
def verifica_diretor(diretores, dir):
    dir = unidecode(dir).replace("'", '')
    if dir not in diretores:
        diretores.append(dir)

# Função para verificar e adicionar filmes únicos à lista
def verifica_filme(filmes, filme, ano, rating, classificacao):
    filme = unidecode(filme).replace("'", "").replace('"', '')
    cert = classifica(classificacao)
    if filme[0].isnumeric():
        titulo = f'The{filme}_{ano}_{rating}_{cert}'
    else:
        titulo = f'{filme}_{ano}_{rating}_{cert}'
    if titulo not in filmes:
        filmes.append(titulo)

# Função para verificar e adicionar gêneros únicos à lista
def verifica_genero(generos, genres):
    for genre in genres.split(','):
        genre = unidecode(genre.strip())
        if genre not in generos:
            generos.append(genre)

# Processa cada linha do DataFrame
for indice, linha in df.iterrows():
    verifica_filme(filmes, linha['Title'], linha['Released_Year'], linha['IMDB_Rating'], linha['Certificate'])
    verifica_diretor(diretores, linha['Director'])
    verifica_ator(atores, linha['Star1'], linha['Star2'], linha['Star3'], linha['Star4'])
    verifica_genero(generos, linha['Genre'])
    #if indice >= 150:
     #   break

# Divide a lista de filmes em colunas separadas
filmes = [filme.split("_") for filme in filmes]

# Cria DataFrames a partir das listas
df_filme = pd.DataFrame(filmes, columns=['Title', 'Released_Year', 'Rating', 'Certificate'])
df_diretor = pd.DataFrame(diretores, columns=['Nome'])
df_ator = pd.DataFrame(atores, columns=['Nome'])
df_genero = pd.DataFrame(generos, columns=['Genero'])

# Salva os DataFrames resultantes em arquivos CSV
df_filme.to_csv('filmes.csv', index=False, encoding='utf-8')
df_diretor.to_csv('diretores.csv', index=False, encoding='utf-8')
df_ator.to_csv('atores.csv', index=False, encoding='utf-8')
df_genero.to_csv('generos.csv', index=False, encoding='utf-8')

# Imprime o DataFrame resultante após as operações de limpeza e renomeação
print(df_filme)
