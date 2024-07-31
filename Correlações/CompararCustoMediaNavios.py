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

# Inicializar dicionário para armazenar a soma das médias dos diferentes tipos de custo
custos_medios_somados = {}

# Calcular a soma das médias dos diferentes tipos de custo para cada tipo de navio
for nome, df in dfs_navios.items():
    media_custos = df.groupby('Tipo de Custo')['Valor (USD)'].mean()
    soma_medias_custos = media_custos.sum()
    custos_medios_somados[nome] = soma_medias_custos

# Criar a tabela comparativa
tabela_comparativa = pd.DataFrame(
    list(custos_medios_somados.items()),
    columns=['Tipo de Navio', 'Soma das Médias dos Custos (USD)']
)

# Salvar a tabela comparativa em um arquivo CSV
tabela_comparativa.to_csv('tabela_comparativa_custos_navios.csv', index=False)

# Gerar gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(tabela_comparativa['Tipo de Navio'], tabela_comparativa['Soma das Médias dos Custos (USD)'], color='skyblue')
plt.xlabel('Tipo de Navio')
plt.ylabel('Soma das Médias dos Custos (USD)')
plt.title('Comparação dos Custos Médios Totais por Tipo de Navio')
plt.xticks(rotation=45)
plt.tight_layout()

# Salvar o gráfico de barras
plt.savefig('comparacao_custos_navios.png')
plt.show()

print("Tabela comparativa salva como 'tabela_comparativa_custos_navios.csv'")
print("Gráfico de barras salvo como 'comparacao_custos_navios.png'")
