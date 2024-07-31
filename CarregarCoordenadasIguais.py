import pandas as pd
from sqlalchemy import create_engine
import urllib.parse

# Caminho para o arquivo CSV
file_coordenadas_iguais = '\\coordenadas_iguais.csv'

# Carregar o arquivo CSV para um DataFrame pandas
df = pd.read_csv(file_coordenadas_iguais)

# Configuração para conectar ao banco de dados MySQL
# Encode a senha para lidar com caracteres especiais
password = urllib.parse.quote_plus('XXXX')

# Conectar ao banco de dados específico (substitua com suas configurações)
engine = create_engine(f'mysql+pymysql://root:{password}@localhost:3306/logistics_db')

# Carregar o arquivo CSV para um DataFrame pandas
df = pd.read_csv('C:\\Users\\thiag\\Downloads\\Desafio_Log\\Insights\\coordenadas_iguais.csv')

# Renomear colunas duplicadas no DataFrame
df.rename(columns={'latitude': 'latitude_df', 'longitude': 'longitude_df'}, inplace=True)

# Nome da tabela no banco de dados
coordenadas_iguais = 'coordenadas_iguais'

# Escrever os dados no banco de dados
df.to_sql(coordenadas_iguais, con=engine, if_exists='append', index=False)

print("Dados importados com sucesso para o banco de dados!")
