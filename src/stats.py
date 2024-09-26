import os
import csv
import statistics


root_directory = r"D:\Pedro\puc\6Semestre\Laboratorio\Analyze-java-repositories\output"


output_file = "dados_agrupados.csv"


data = []

# Percorre todas as pastas e arquivos
for foldername, subfolders, filenames in os.walk(root_directory):
    for filename in filenames:
        if filename == "class.csv":
            file_path = os.path.join(foldername, filename)
            
            
            folder_name = os.path.basename(foldername)
            
            loc_list = []
            cbo_list = []
            dit_list = []
            lcom_list = []
            
            
            with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                
                for row in csv_reader:
                    
                    try:
                        loc_list.append(float(row['loc']))
                        cbo_list.append(float(row['cbo']))
                        dit_list.append(float(row['dit']))
                        lcom_list.append(float(row['lcom']))
                    except ValueError:
                        continue
            
            # Função para calcular moda com tratamento de exceção
            def safe_mode(lst):
                try:
                    return statistics.mode(lst)
                except statistics.StatisticsError:
                    return 'N/A'  

            # Função para calcular média, mediana e moda ou retornar N/A se a lista estiver vazia
            def calculate_statistics(lst):
                if lst:
                    return (statistics.mean(lst), statistics.median(lst), safe_mode(lst))
                else:
                    return ('N/A', 'N/A', 'N/A')
            
            # Calcula as estatísticas para loc, cbo, dit e lcom
            loc_mean, loc_median, loc_mode = calculate_statistics(loc_list)
            cbo_mean, cbo_median, cbo_mode = calculate_statistics(cbo_list)
            dit_mean, dit_median, dit_mode = calculate_statistics(dit_list)
            lcom_mean, lcom_median, lcom_mode = calculate_statistics(lcom_list)
            
            data.append([folder_name, loc_mean, loc_median, loc_mode, 
                         cbo_mean, cbo_median, cbo_mode, 
                         dit_mean, dit_median, dit_mode, 
                         lcom_mean, lcom_median, lcom_mode])

# Escreve os dados processados em um novo arquivo CSV
with open(output_file, mode='w', newline='', encoding='utf-8') as output_csv:
    csv_writer = csv.writer(output_csv)
    
    csv_writer.writerow([
        'nome_da_pasta', 
        'loc_media', 'loc_mediana', 'loc_moda', 
        'cbo_media', 'cbo_mediana', 'cbo_moda', 
        'dit_media', 'dit_mediana', 'dit_moda', 
        'lcom_media', 'lcom_mediana', 'lcom_moda'])
    
    csv_writer.writerows(data)

print(f"Dados extraídos e processados com sucesso em {output_file}")
