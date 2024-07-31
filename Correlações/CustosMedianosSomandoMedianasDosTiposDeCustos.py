import pandas as pd
import matplotlib.pyplot as plt

# Caminhos para os arquivos CSV dos navios
caminhos_navios = {
  "carga_geral": '//Desafio_Log//navio_carga_geral.csv',
    "frigirorifico": '//Desafio_Log//navio_frigorifico.csv',
    "graneleiro": '//Desafio_Log//navio_graneleiro.csv',
    "porta_conteiner": '//Desafio_Log//navio_porta_conteiner.csv',
    "ro_ro": '//Desafio_Log//navio_ro_ro.csv'
}

# Carregar os dados dos navios em dataframes
dfs_navios = {nome: pd.read_csv(caminho) for nome, caminho in caminhos_navios.items()}

# Concatenar todos os dataframes em um único dataframe
df_todos_navios = pd.concat(dfs_navios.values(), ignore_index=True)

# Calcular a mediana dos custos para cada tipo de custo e porto
custos_medianas_portos = df_todos_navios.groupby(['Porto', 'Tipo de Custo'])['Valor (USD)'].median().reset_index()

# Calcular a soma das medianas dos custos por porto
custos_medianas_totais_portos = custos_medianas_portos.groupby('Porto')['Valor (USD)'].sum().reset_index()

# Renomear as colunas para a tabela comparativa
custos_medianas_totais_portos.columns = ['Porto', 'Mediana Total (USD)']

# Salvar a tabela comparativa em um arquivo CSV
custos_medianas_totais_portos.to_csv('//tabela_comparativa_medianas_portos.csv', index=False)

# Gerar gráfico de barras
plt.figure(figsize=(12, 8))
plt.bar(custos_medianas_totais_portos['Porto'], custos_medianas_totais_portos['Mediana Total (USD)'], color='skyblue')
plt.xlabel('Porto')
plt.ylabel('Mediana Total (USD)')
plt.title('Comparação das Medianas Totais por Porto')
plt.xticks(rotation=45)
plt.tight_layout()

# Salvar o gráfico de barras
plt.savefig('//comparacao_medianas_portos.png')
plt.show()

print("Tabela comparativa salva como 'tabela_comparativa_medianas_portos.csv'")
print("Gráfico de barras salvo como 'comparacao_medianas_portos.png'")
