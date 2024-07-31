import pandas as pd

# Caminho para os arquivos CSV
files = {
    'multas_portuarias': '\\multas_portuarias_atualizado.csv',
    'portos': '\\Desafio_Log\\portos.csv',
    'rotas': 'g\\rotas.csv',
    'taxas_portuarias': '\\taxas_portuarias.csv'
}

# Ler os arquivos CSV para DataFrames
df_multas_portuarias = pd.read_csv(files['multas_portuarias'])
df_portos = pd.read_csv(files['portos'])
df_rotas = pd.read_csv(files['rotas'])
df_taxas_portuarias = pd.read_csv(files['taxas_portuarias'])

# Exibir as primeiras linhas de cada DataFrame para verificação
print(df_multas_portuarias.head())
print(df_portos.head())
print(df_rotas.head())
print(df_taxas_portuarias.head())

# Função para padronizar os dados
def padronizar_dados(df):
    # Tratar valores ausentes
    df.fillna(0, inplace=True)
    
    # Posso adicionar outras transformações específicas aqui
    return df

# Aplicar a função de padronização em cada DataFrame
df_multas_portuarias = padronizar_dados(df_multas_portuarias)
df_portos = padronizar_dados(df_portos)
df_rotas = padronizar_dados(df_rotas)
df_taxas_portuarias = padronizar_dados(df_taxas_portuarias)

# Exibir os primeiros registros de um dos DataFrames transformados para verificação
print(df_multas_portuarias.head())
print(df_portos.head())
print(df_rotas.head())
print(df_taxas_portuarias.head())

from sqlalchemy import create_engine
import urllib.parse

# Encode the password to handle special characters
password = urllib.parse.quote_plus('XXXX')


# Conectar ao banco de dados específico
db_engine = create_engine(f'mysql+pymysql://root:{password}@localhost:3306/logistics_db')

# Função para carregar DataFrame para SQL
def carregar_para_sql(df, tabela_nome):
    df.to_sql(tabela_nome, con=db_engine, if_exists='replace', index=False)

# Carregar cada DataFrame para uma tabela no banco de dados
carregar_para_sql(df_multas_portuarias, 'multas_portuarias')
carregar_para_sql(df_portos, 'portos')
carregar_para_sql(df_rotas, 'rotas')
carregar_para_sql(df_taxas_portuarias, 'taxas_portuarias')

print("Dados carregados com sucesso para o banco de dados SQL!")

# Função para executar uma consulta SQL e retornar um DataFrame
def executar_consulta(sql_query):
    with db_engine.connect() as connection:
       result = pd.read_sql(sql_query, connection)
    return result

 #Consulta para visualizar as tabelas criadas
tabelas = executar_consulta("SHOW TABLES;")
print(tabelas)

# Consulta para visualizar os dados de uma tabela específica
df_multas_portuarias = executar_consulta("SELECT * FROM multas_portuarias LIMIT 10;")
print(df_multas_portuarias)

df_portos = executar_consulta("SELECT * FROM portos LIMIT 10;")
print(df_portos)

df_rotas = executar_consulta("SELECT * FROM rotas LIMIT 100;")
print(df_rotas)

df_taxas_portuarias = executar_consulta("SELECT * FROM taxas_portuarias LIMIT 10;")
print(df_taxas_portuarias)

