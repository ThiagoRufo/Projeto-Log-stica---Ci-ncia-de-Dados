import pandas as pd

# Carregar os dados dos CSVs dos navios
caminhos_navios = {
    "carga_geral": '//Desafio_Log//navio_carga_geral.csv',
    "frigirorifico": '//Desafio_Log//navio_frigorifico.csv',
    "graneleiro": 's//Desafio_Log//navio_graneleiro.csv',
    "porta_conteiner": '//Desafio_Log//navio_porta_conteiner.csv',
    "ro_ro": '//Desafio_Log//navio_ro_ro.csv'
}

dfs_navios = {nome: pd.read_csv(caminho) for nome, caminho in caminhos_navios.items()}

# Calcula o custo médio ponderado pelo volume
custos_ponderados = {}
for nome, df in dfs_navios.items():
    # Filtrar linhas onde o volume é válido
    df_valid = df.dropna(subset=['Volume'])
    # Calcular o custo total ponderado e o volume total
    custo_total_ponderado = (df_valid['Valor (USD)'] * df_valid['Volume']).sum()
    volume_total = df_valid['Volume'].sum()
    # Calcular o custo médio ponderado
    custo_medio_ponderado = custo_total_ponderado / volume_total if volume_total else 0
    custos_ponderados[nome] = custo_medio_ponderado

# Criar a tabela comparativa
tabela_comparativa_ponderada = pd.DataFrame(
    list(custos_ponderados.items()),
    columns=['Tipo de Navio', 'Custo Médio Ponderado (USD)']
)

print(tabela_comparativa_ponderada)
