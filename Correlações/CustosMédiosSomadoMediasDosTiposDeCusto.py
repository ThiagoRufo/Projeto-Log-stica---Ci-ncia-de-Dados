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

# Calcular a média dos custos para cada tipo de custo e porto
custos_medios_portos = df_todos_navios.groupby(['Porto', 'Tipo de Custo'])['Valor (USD)'].mean().reset_index()

# Calcular a soma das médias dos custos por porto
custos_medios_totais_portos = custos_medios_portos.groupby('Porto')['Valor (USD)'].sum().reset_index()

# Renomear as colunas para a tabela comparativa
custos_medios_totais_portos.columns = ['Porto', 'Custo Médio Total (USD)']

# Salvar a tabela comparativa em um arquivo CSV
custos_medios_totais_portos.to_csv('//CorrelaçõesNavios//tabela_comparativa_custos_portos.csv', index=False)

# Gerar gráfico de barras
plt.figure(figsize=(12, 8))
plt.bar(custos_medios_totais_portos['Porto'], custos_medios_totais_portos['Custo Médio Total (USD)'], color='skyblue')
plt.xlabel('Porto')
plt.ylabel('Custo Médio Total (USD)')
plt.title('Comparação dos Custos Médios Totais por Porto')
plt.xticks(rotation=45)
plt.tight_layout()

# Salvar o gráfico de barras
plt.savefig('//CorrelaçõesNavios//comparacao_custos_medios_totais_portos.png')
plt.show()

print("Tabela comparativa salva como 'tabela_comparativa_custos_portos.csv'")
print("Gráfico de barras salvo como 'comparacao_custos_medios_totais_portos.png'")


