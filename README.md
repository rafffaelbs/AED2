# AED2

## Explicação geral
O seguinte repositório é uma ferramenta para recomendação de filmes, baseado em outros filmes assistidos, utilizando grafos.

## Arquivos
Cada arquivo do repositório é responsável por uma certa coisa.

transforma.py: Esse código lê um arquivo CSV com os 1000 filmes mais bem avaliados do IMDB, remove colunas desnecessárias, renomeia a coluna 'Series_Title' para 'Title', e define funções para padronizar classificações indicativas, verificar e adicionar atores, diretores, filmes e gêneros únicos a listas; ao final, cria DataFrames a partir dessas listas e salva-os em arquivos CSV separados para filmes, diretores, atores e gêneros.

cria.py: 

envia.py:

requisições.py:
