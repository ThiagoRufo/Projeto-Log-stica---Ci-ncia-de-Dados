import pandas as pd
from sqlalchemy import create_engine
import urllib.parse

# Caminhos para os arquivos CSV convertidos
files = [
    '\\navio_ro_ro.csv',
    '\\navio_porta_conteiner.csv',
    '\\navio_graneleiro.csv',
    '\\navio_frigorifico.csv',
    '\\navio_carga_geral.csv'
]

# Lista para armazenar os DataFrames
dataframes = []

# Carregar cada arquivo CSV para um DataFrame
for file in files:
    df = pd.read_csv(file)
    dataframes.append(df)

# Função para padronizar os dados (se necessário)
def padronizar_dados(df):
    # Exemplo: tratar valores ausentes
    df.fillna(0, inplace=True)
    return df

# Aplicar a função de padronização (se necessário)
for i, df in enumerate(dataframes):
    dataframes[i] = padronizar_dados(df)

# Exibir os primeiros registros de um dos DataFrames para verificação
print(dataframes[0].head())

# Configuração para conectar ao banco de dados MySQL
# Encode a senha para lidar com caracteres especiais
password = urllib.parse.quote_plus('Pudin@00')

# Conectar ao banco de dados específico (substitua com suas configurações)
db_engine = create_engine(f'mysql+pymysql://root:{password}@localhost:3306/logistics_db')

# Função para carregar DataFrame para SQL
def carregar_para_sql(df, tabela_nome):
    df.to_sql(tabela_nome, con=db_engine, if_exists='replace', index=False)

# Nomes das tabelas correspondentes aos arquivos CSV
nomes_tabelas = [
    'navio_ro_ro',
    'navio_porta_conteiner',
    'navio_graneleiro',
    'navio_frigorifico',
    'navio_carga_geral'
]

# Carregar cada DataFrame para uma tabela no banco de dados
for i, df in enumerate(dataframes):
    carregar_para_sql(df, nomes_tabelas[i])

print("Dados carregados com sucesso para o banco de dados SQL!")
