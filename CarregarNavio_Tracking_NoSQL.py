import pandas as pd
from sqlalchemy import create_engine
import urllib.parse

# Caminho para o arquivo CSV
file_navio_tracking = '\\navio_tracking.csv'

# Carregar o arquivo CSV para um DataFrame
df_navio_tracking = pd.read_csv(file_navio_tracking, delimiter=';')  # Ajuste o delimitador conforme necessário

# Exibir as primeiras linhas do DataFrame para verificação
print(df_navio_tracking.head())

# Função para padronizar os dados (se necessário)
def padronizar_dados(df):
    # Exemplo: tratar valores ausentes
    df.fillna(0, inplace=True)
    return df

# Aplicar a função de padronização (se necessário)
df_navio_tracking = padronizar_dados(df_navio_tracking)

# Configuração para conectar ao banco de dados MySQL
# Encode a senha para lidar com caracteres especiais
password = urllib.parse.quote_plus('XXXX')

# Conectar ao banco de dados específico (substitua com suas configurações)
db_engine = create_engine(f'mysql+pymysql://root:{password}@localhost:3306/logistics_db')

# Nome da tabela correspondente ao arquivo CSV
nome_tabela = 'navio_tracking'

# Função para carregar DataFrame para SQL
def carregar_para_sql(df, tabela_nome):
    df.to_sql(tabela_nome, con=db_engine, if_exists='replace', index=False)

# Carregar o DataFrame para a tabela no banco de dados
carregar_para_sql(df_navio_tracking, nome_tabela)

print(f"Dados do arquivo '{file_navio_tracking}' carregados com sucesso para a tabela '{nome_tabela}' no banco de dados SQL!")


