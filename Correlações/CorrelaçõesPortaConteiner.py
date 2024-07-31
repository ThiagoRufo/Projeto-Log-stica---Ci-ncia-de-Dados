import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import urllib

# Definindo a senha e criando a URL de conexão
password = urllib.parse.quote_plus('XXXX')
engine = create_engine(f'mysql+pymysql://root:{password}@localhost:3306/logistics_db')

# Carregando os dados da tabela SQL para um DataFrame
table_name = 'navio_porta_conteiner'
navio_porta_conteiner_df = pd.read_sql_table(table_name, engine)

# Exibir as primeiras linhas do DataFrame para verificar o carregamento
print(navio_porta_conteiner_df.head())

# Função para identificar e remover outliers usando o método IQR
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Remover outliers na coluna 'Valor (USD)'
navio_porta_conteiner_clean_df = remove_outliers(navio_porta_conteiner_df, 'Valor (USD)')

# Medidas de dispersão e posição
measures_of_dispersion = navio_porta_conteiner_clean_df['Valor (USD)'].describe()

# Adicionar mais medidas de dispersão
measures_of_dispersion['variance'] = navio_porta_conteiner_clean_df['Valor (USD)'].var()
measures_of_dispersion['range'] = measures_of_dispersion['max'] - measures_of_dispersion['min']
measures_of_dispersion['iqr'] = measures_of_dispersion['75%'] - measures_of_dispersion['25%']

# Custos médios por navio
avg_cost_per_ship_clean = navio_porta_conteiner_clean_df.groupby('Nome do Navio')['Valor (USD)'].mean()

# Custos médios por porto
avg_cost_per_port_clean = navio_porta_conteiner_clean_df.groupby('Porto')['Valor (USD)'].mean()

# Custos médios por tipo de custo
avg_cost_per_cost_type_clean = navio_porta_conteiner_clean_df.groupby('Tipo de Custo')['Valor (USD)'].mean()

# Gráfico de custos médios por navio
plt.figure(figsize=(10, 6))
sns.barplot(x=avg_cost_per_ship_clean.index, y=avg_cost_per_ship_clean.values)
plt.xticks(rotation=90)
plt.title('Custos Médios por Navio (Navio Porta Conteiner, sem outliers)')
plt.ylabel('Valor Médio (USD)')
plt.xlabel('Nome do Navio')
plt.show()

# Gráfico de custos médios por porto
plt.figure(figsize=(10, 6))
sns.barplot(x=avg_cost_per_port_clean.index, y=avg_cost_per_port_clean.values)
plt.xticks(rotation=90)
plt.title('Custos Médios por Porto (Navio Porta Conteiner, sem outliers)')
plt.ylabel('Valor Médio (USD)')
plt.xlabel('Porto')
plt.show()

# Gráfico de custos médios por tipo de custo
plt.figure(figsize=(10, 6))
sns.barplot(x=avg_cost_per_cost_type_clean.index, y=avg_cost_per_cost_type_clean.values)
plt.xticks(rotation=90)
plt.title('Custos Médios por Tipo de Custo (Navio Porta Conteiner, sem outliers)')
plt.ylabel('Valor Médio (USD)')
plt.xlabel('Tipo de Custo')
plt.show()

# Exibir a tabela de medidas de dispersão
print(measures_of_dispersion)

# Adicionar a tabela de medidas de dispersão a um DataFrame
dispersion_df = pd.DataFrame(measures_of_dispersion).transpose()

# Exibir a tabela de medidas de dispersão
print(dispersion_df)

# Salvar o DataFrame em um arquivo CSV
dispersion_df.to_csv('medidas_dispersao_porta_conteiner.csv', index=False)

# Salvar o DataFrame em uma tabela SQL
dispersion_df.to_sql('medidas_dispersao_porta_conteiner', con=engine, if_exists='replace', index=False)
