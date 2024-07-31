import pandas as pd
from sqlalchemy import create_engine
import urllib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Definindo a senha e criando a URL de conexão
password = urllib.parse.quote_plus('XXXX')
engine = create_engine(f'mysql+pymysql://root:{password}@localhost:3306/logistics_db')

# Função para identificar e remover outliers usando o método IQR
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Função para processar as tabelas e calcular os custos médios por tipo de custo e navio
def process_table(table_name):
    # Carregando os dados da tabela SQL para um DataFrame
    df = pd.read_sql_table(table_name, engine)
    
    # Remover outliers na coluna 'Valor (USD)'
    df_clean = remove_outliers(df, 'Valor (USD)')
    
    # Custos médios por tipo de custo para cada navio
    avg_cost_per_ship_and_cost_type = df_clean.groupby(['Nome do Navio', 'Tipo de Custo'])['Valor (USD)'].mean().reset_index()
    
    # Exibir o DataFrame com os custos médios por tipo de custo para cada navio
    print(f"Custos médios por tipo de custo para {table_name}:")
    print(avg_cost_per_ship_and_cost_type)
    
    # Salvar o DataFrame em um arquivo CSV
    avg_cost_per_ship_and_cost_type.to_csv(f'custos_medios_por_tipo_custo_por_{table_name}.csv', index=False)
    
    return avg_cost_per_ship_and_cost_type

# Tabelas a serem processadas
tables = ['navio_carga_geral', 'navio_frigorifico', 'navio_graneleiro', 'navio_porta_conteiner', 'navio_ro_ro']

# Processar cada tabela e armazenar os resultados em um dicionário
results = {}
for table in tables:
    results[table] = process_table(table)
