import pandas as pd

# Lista dos nomes dos arquivos XLSX
arquivos_xlsx = [
    '\\navio_ro_ro.xlsx',
    '\\navio_porta_conteiner.xlsx',
    '\\navio_graneleiro.xlsx',
    '\\navio_frigorifico.xlsx',
    '\\navio_carga_geral.xlsx'
]

# Converter cada arquivo XLSX para CSV
for arquivo in arquivos_xlsx:
    # Carregar o arquivo XLSX
    df = pd.read_excel(arquivo)
    
    # Extrair o nome do arquivo sem a extensão
    nome_csv = arquivo.split('.')[0] + '.csv'
    
    # Salvar como CSV
    df.to_csv(nome_csv, index=False)
    print(f'Arquivo {nome_csv} convertido com sucesso.')

print("Todos os arquivos foram convertidos para CSV.")
