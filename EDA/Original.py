import pandas as pd

# Elimina as tabelas do CSV original que não usaremos
df = pd.read_csv('C:/Users/rafae/Code/Outros/Python/Projetos/Neo4j/imdb_top_1000.csv')

df = df.drop(columns=['Gross'])
df = df.drop(columns=['Runtime'])
df = df.drop(columns=['No_of_Votes'])
df = df.drop(columns=['Overview'])
df = df.drop(columns=['Meta_score'])
df = df.drop(columns=['Poster_Link'])

# Muda nome da Coluna Series_Title para Title e transforma o df resultante em um novo CSV
print("\nDataFrame agrupado por 'Categoria' com soma das vendas e quantidade:")
df= df.rename(columns={'Series_Title':'Title'})
print(df)
df.to_csv('imdb.csv', index=False, encoding='utf-8')


# Verifica quais são todas as Classificações Indicativas Presentes no dataset
df = pd.read_csv('C:/Users/rafae/Code/Outros/Python/Projetos/Neo4j/imdb.csv')
grouped = df.groupby('Certificate')

certificates = df['Certificate'].unique()

# Print the unique certificates
print("Unique Certificates:")
for cert in certificates:
    print(cert)
