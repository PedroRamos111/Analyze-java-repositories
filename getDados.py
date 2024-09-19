import os
import csv

# Caminho da pasta raiz onde estão as subpastas
root_directory = r"D:\Pedro\puc\6Semestre\Laboratorio\Analyze-java-repositories\output"

# Nome do arquivo de saída
output_file = "dados.csv"

# Lista para armazenar os dados extraídos
data = []

# Percorre todas as pastas e arquivos
for foldername, subfolders, filenames in os.walk(root_directory):
    for filename in filenames:
        if filename == "class.csv":
            file_path = os.path.join(foldername, filename)
            
            # Nome da pasta
            folder_name = os.path.basename(foldername)
            
            # Abrir e ler o arquivo CSV
            with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                
                for row in csv_reader:
                    # Extrai os dados necessários
                    loc = row['loc']
                    cbo = row['cbo']
                    dit = row['dit']
                    lcom = row['lcom']
                    
                    # Adiciona os dados à lista
                    data.append([folder_name, loc, cbo, dit, lcom])

# Escreve os dados extraídos em um novo arquivo CSV
with open(output_file, mode='w', newline='', encoding='utf-8') as output_csv:
    csv_writer = csv.writer(output_csv)
    
    # Escreve o cabeçalho
    csv_writer.writerow(['nome_da_pasta', 'loc', 'cbo', 'dit', 'lcom'])
    
    # Escreve os dados
    csv_writer.writerows(data)

print(f"Dados extraídos e salvos em {output_file}")
