import pandas as pd
import matplotlib.pyplot as plt

# Caminhos para os arquivos CSV dos navios
caminhos_navios = {
    "carga_geral": '//navio_carga_geral.csv',
    "frigirorifico": '//navio_frigorifico.csv',
    "graneleiro": '//navio_graneleiro.csv',
    "porta_conteiner": '//navio_porta_conteiner.csv',
    "ro_ro": '//navio_ro_ro.csv'
}

# Carregar os dados dos navios em dataframes
dfs_navios = {nome: pd.read_csv(caminho) for nome, caminho in caminhos_navios.items()}

# Inicializar dicionário para armazenar a soma das medianas dos diferentes tipos de custo
custos_medianas_somados = {}

# Calcular a soma das medianas dos diferentes tipos de custo para cada tipo de navio
for nome, df in dfs_navios.items():
    mediana_custos = df.groupby('Tipo de Custo')['Valor (USD)'].median()
    soma_medianas_custos = mediana_custos.sum()
    custos_medianas_somados[nome] = soma_medianas_custos

# Criar a tabela comparativa
tabela_comparativa = pd.DataFrame(
    list(custos_medianas_somados.items()),
    columns=['Tipo de Navio', 'Soma das Medianas dos Custos (USD)']
)

# Salvar a tabela comparativa em um arquivo CSV
tabela_comparativa.to_csv('tabela_comparativa_custos_navios_medianas.csv', index=False)

# Gerar gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(tabela_comparativa['Tipo de Navio'], tabela_comparativa['Soma das Medianas dos Custos (USD)'], color='skyblue')
plt.xlabel('Tipo de Navio')
plt.ylabel('Soma das Medianas dos Custos (USD)')
plt.title('Comparação dos Custos Medianos Totais por Tipo de Navio')
plt.xticks(rotation=45)
plt.tight_layout()

# Salvar o gráfico de barras
plt.savefig('comparacao_custos_navios_medianas.png')
plt.show()

print("Tabela comparativa salva como 'tabela_comparativa_custos_navios_medianas.csv'")
print("Gráfico de barras salvo como 'comparacao_custos_navios_medianas.png'")
