import pandas as pd
import matplotlib.pyplot as plt

# Caminhos para os arquivos CSV dos navios
caminhos_navios = {
    "carga_geral": '//Desafio_Log//navio_carga_geral.csv',
    "frigirorifico": '//Desafio_Log//navio_frigorifico.csv',
    "graneleiro": '//Desafio_Log//navio_graneleiro.csv',
    "porta_conteiner": 's//Desafio_Log//navio_porta_conteiner.csv',
    "ro_ro": '//Desafio_Log//navio_ro_ro.csv'
}

# Carregar os dados dos navios em dataframes
dfs_navios = {nome: pd.read_csv(caminho) for nome, caminho in caminhos_navios.items()}

# Concatenar todos os dataframes em um único dataframe
df_todos_navios = pd.concat(dfs_navios.values(), ignore_index=True)

# Calcular a média dos custos para cada porto
custos_medios_portos = df_todos_navios.groupby('Porto')['Valor (USD)'].mean().reset_index()

# Renomear as colunas para a tabela comparativa
custos_medios_portos.columns = ['Porto', 'Custo Médio Total (USD)']

# Salvar a tabela comparativa em um arquivo CSV
custos_medios_portos.to_csv('tabela_comparativa_custos_portos.csv', index=False)

# Gerar gráfico de barras
plt.figure(figsize=(12, 8))
plt.bar(custos_medios_portos['Porto'], custos_medios_portos['Custo Médio Total (USD)'], color='skyblue')
plt.xlabel('Porto')
plt.ylabel('Custo Médio Total (USD)')
plt.title('Comparação dos Custos Médios Totais por Porto')
plt.xticks(rotation=45)
plt.tight_layout()

# Salvar o gráfico de barras
plt.savefig('comparacao_custos_portos.png')
plt.show()

print("Tabela comparativa salva como 'tabela_comparativa_custos_portos.csv'")
print("Gráfico de barras salvo como 'comparacao_custos_portos.png'")

# Calcular a mediana dos custos para cada porto
custos_medianos_portos = df_todos_navios.groupby('Porto')['Valor (USD)'].median().reset_index()

# Renomear as colunas para a tabela comparativa
custos_medianos_portos.columns = ['Porto', 'Custo Mediano Total (USD)']

# Salvar a tabela comparativa em um arquivo CSV
custos_medianos_portos.to_csv('tabela_comparativa_custos_portos.csv', index=False)

# Gerar gráfico de barras
plt.figure(figsize=(12, 8))
plt.bar(custos_medianos_portos['Porto'], custos_medianos_portos['Custo Mediano Total (USD)'], color='skyblue')
plt.xlabel('Porto')
plt.ylabel('Custo Mediano Total (USD)')
plt.title('Comparação dos Custos Medianos Totais por Porto')
plt.xticks(rotation=45)
plt.tight_layout()

# Salvar o gráfico de barras
plt.savefig('comparacao_custos_portos.png')
plt.show()

print("Tabela comparativa salva como 'tabela_comparativa_custos_portos.csv'")
print("Gráfico de barras salvo como 'comparacao_custos_portos.png'")
