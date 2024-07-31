
import pandas as pd
from geopy.distance import geodesic

# Carregar as tabelas de CSV para DataFrames
portos_df = pd.read_csv('\\portos.csv')
navio_tracking_df = pd.read_csv('\\navio_tracking.csv', delimiter=';')

# Ajustar os nomes das colunas
latitude_col_portos = 'Latitude'
longitude_col_portos = 'Longitude'
latitude_col_navio = 'latitude'
longitude_col_navio = 'longitude'

# Definir uma função para encontrar linhas com coordenadas geográficas iguais
def encontrar_coordenadas_iguais(portos_df, navio_tracking_df, tolerancia=0.001):
    linhas_iguais = []

    for _, porto in portos_df.iterrows():
        porto_coords = (porto[latitude_col_portos], porto[longitude_col_portos])
        
        for _, navio in navio_tracking_df.iterrows():
            navio_coords = (navio[latitude_col_navio], navio[longitude_col_navio])
            distancia = geodesic(porto_coords, navio_coords).kilometers
            
            if distancia <= tolerancia:
                linha_combinada = porto.to_dict()
                linha_combinada.update(navio.to_dict())
                linhas_iguais.append(linha_combinada)
                
    return pd.DataFrame(linhas_iguais)

# Encontrar linhas com coordenadas iguais
result_df = encontrar_coordenadas_iguais(portos_df, navio_tracking_df)

# Salvar o resultado em um novo arquivo CSV
result_df.to_csv('coordenadas_iguais.csv', index=False)

print("As linhas com coordenadas iguais foram salvas em 'coordenadas_iguais.csv'.")

