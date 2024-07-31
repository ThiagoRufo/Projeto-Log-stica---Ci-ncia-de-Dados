import pandas as pd
import matplotlib.pyplot as plt

# Carregar os arquivos CSV
df_navio_carga_geral = pd.read_csv('\\navio_carga_geral.csv')
df_navio_frigorifico = pd.read_csv('\\navio_frigorifico.csv')
df_navio_graneleiro = pd.read_csv('\\navio_graneleiro.csv')
df_navio_porta_conteiner = pd.read_csv('\\navio_porta_conteiner.csv')
df_navio_ro_ro = pd.read_csv('\\navio_ro_ro.csv')
df_rotas = pd.read_csv('\\rotas.csv')

# Função para calcular o custo médio de combustível por milha náutica
def calcular_custo_medio_combustivel(df, tipo_navio):
    # Filtrar os custos de combustível
    df_combustivel = df[df['Tipo de Custo'] == 'Combustível']
    
    # Ordenar os registros por nome do navio e data
    df = df.sort_values(by=['Nome do Navio', 'Data'])
    
    # Inicializar listas para armazenar os resultados
    navios = []
    tipos_navio = []
    custos_medios = []
    
    # Obter a lista de navios únicos
    navios_unicos = df['Nome do Navio'].unique()
    
    for navio in navios_unicos:
        # Filtrar os registros do navio
        df_navio = df[df['Nome do Navio'] == navio]
        
        # Inicializar variáveis para armazenar o custo total de combustível e a distância total percorrida
        custo_total_combustivel = df_combustivel[df_combustivel['Nome do Navio'] == navio]['Valor (USD)'].sum()
        distancia_total = 0
        
        # Iterar sobre os registros do navio para calcular a distância percorrida
        for i in range(len(df_navio) - 1):
            porto_origem = df_navio.iloc[i]['Porto']
            porto_destino = df_navio.iloc[i + 1]['Porto']
            
            # Obter a distância entre os portos de origem e destino da tabela de rotas
            rota = df_rotas[(df_rotas['Porto_Origem'] == porto_origem) & (df_rotas['Porto_Destino'] == porto_destino)]
            if rota.empty:
                rota = df_rotas[(df_rotas['Porto_Origem'] == porto_destino) & (df_rotas['Porto_Destino'] == porto_origem)]
            
            if not rota.empty:
                distancia = rota['Distancia'].values[0]
                distancia_total += distancia
        
        # Calcular o custo médio de combustível por milha náutica
        if distancia_total > 0:
            custo_medio_combustivel = custo_total_combustivel / distancia_total
            navios.append(navio)
            tipos_navio.append(tipo_navio)
            custos_medios.append(custo_medio_combustivel)
    
    # Criar um DataFrame com os resultados
    df_resultado = pd.DataFrame({
        'Nome do Navio': navios,
        'Tipo de Navio': tipos_navio,
        'Custo Médio por Milha Náutica': custos_medios
    })
    
    return df_resultado

# Calcular o custo médio de combustível por milha náutica para cada tipo de navio
df_custo_medio_carga_geral = calcular_custo_medio_combustivel(df_navio_carga_geral, 'Carga Geral')
df_custo_medio_frigorifico = calcular_custo_medio_combustivel(df_navio_frigorifico, 'Frigorífico')
df_custo_medio_graneleiro = calcular_custo_medio_combustivel(df_navio_graneleiro, 'Graneleiro')
df_custo_medio_porta_conteiner = calcular_custo_medio_combustivel(df_navio_porta_conteiner, 'Porta-Contêiner')
df_custo_medio_ro_ro = calcular_custo_medio_combustivel(df_navio_ro_ro, 'Ro-Ro')

# Concatenar todos os resultados em um único DataFrame
df_custo_medio_combustivel = pd.concat([
    df_custo_medio_carga_geral,
    df_custo_medio_frigorifico,
    df_custo_medio_graneleiro,
    df_custo_medio_porta_conteiner,
    df_custo_medio_ro_ro
], ignore_index=True)

# Salvar o DataFrame de custo médio de combustível por milha náutica em um arquivo CSV
df_custo_medio_combustivel.to_csv('custo_medio_combustivel_por_navio.csv', index=False)

# Calcular os custos médios por tipo de navio
df_custo_medio_por_tipo = df_custo_medio_combustivel.groupby('Tipo de Navio')['Custo Médio por Milha Náutica'].mean().reset_index()

# Salvar o DataFrame de custo médio por tipo de navio em um arquivo CSV
df_custo_medio_por_tipo.to_csv('custo_medio_combustivel_por_tipo_de_navio.csv', index=False)

# Exibir os resultados
print("Custo Médio de Combustível por Milha Náutica para Cada Navio:")
print(df_custo_medio_combustivel)
print("\nCusto Médio de Combustível por Milha Náutica por Tipo de Navio:")
print(df_custo_medio_por_tipo)

# Gerar um gráfico de barras para os custos médios por tipo de navio
plt.figure(figsize=(10, 6))
plt.bar(df_custo_medio_por_tipo['Tipo de Navio'], df_custo_medio_por_tipo['Custo Médio por Milha Náutica'], color='skyblue')
plt.xlabel('Tipo de Navio')
plt.ylabel('Custo Médio por Milha Náutica (USD)')
plt.title('Custo Médio de Combustível por Milha Náutica por Tipo de Navio')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('custo_medio_combustivel_por_tipo_de_navio.png')
plt.show()

# Gerar um gráfico de barras para os custos médios por navio
plt.figure(figsize=(14, 8))
plt.bar(df_custo_medio_combustivel['Nome do Navio'], df_custo_medio_combustivel['Custo Médio por Milha Náutica'], color='lightgreen')
plt.xlabel('Nome do Navio')
plt.ylabel('Custo Médio por Milha Náutica (USD)')
plt.title('Custo Médio de Combustível por Milha Náutica por Navio')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('custo_medio_combustivel_por_navio.png')
plt.show()
