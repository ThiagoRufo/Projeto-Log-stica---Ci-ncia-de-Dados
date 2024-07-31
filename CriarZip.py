import zipfile
import os

# Caminho do diretório onde os arquivos CSV estão localizados
caminho_diretorio = '//Desafio_Log//zip'  

# Nome do arquivo ZIP
zip_filename = 'tabelas_banco_de_dados.zip'

# Criar um arquivo ZIP
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    for root, _, files in os.walk(caminho_diretorio):
        for file in files:
            if file.endswith('.csv'):
                zipf.write(os.path.join(root, file), arcname=file)

print(f"Arquivo ZIP criado: {zip_filename}")
