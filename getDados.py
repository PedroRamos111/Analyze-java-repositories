import os
import csv

root_directory = r"D:\Pedro\puc\6Semestre\Laboratorio\Analyze-java-repositories\output"

output_file = "dados.csv"

data = []

# Percorre todas as pastas e arquivos
for foldername, subfolders, filenames in os.walk(root_directory):
    for filename in filenames:
        if filename == "class.csv":
            file_path = os.path.join(foldername, filename)
            
            
            folder_name = os.path.basename(foldername)
            
           
            with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                
                for row in csv_reader:
                    loc = row['loc']
                    cbo = row['cbo']
                    dit = row['dit']
                    lcom = row['lcom']
                    
                    data.append([folder_name, loc, cbo, dit, lcom])

# Escreve os dados extraídos em um novo arquivo CSV
with open(output_file, mode='w', newline='', encoding='utf-8') as output_csv:
    csv_writer = csv.writer(output_csv)

    csv_writer.writerow(['nome_da_pasta', 'loc', 'cbo', 'dit', 'lcom'])

    csv_writer.writerows(data)

print(f"Dados extraídos e salvos em {output_file}")
