# Importa as bibliotecas necessárias
import pandas as pd

# Caminho para o arquivo CSV
file_path = '..\Analyze-java-repositories\DadosRQ.csv'  # Altere para o caminho correto

# Leitura do arquivo CSV com a codificação correta
df = pd.read_csv(file_path, encoding='ISO-8859-1')

# Função para exibir os 5 maiores e menores valores de uma coluna
def exibir_maiores_menores(coluna):
    maiores = df.nlargest(5, coluna)[['Nome do Repositório', coluna]]
    menores = df.nsmallest(5, coluna)[['Nome do Repositório', coluna]]
    return maiores, menores

# 1. 5 maiores e 5 menores repositórios em termos de estrelas
maiores_estrelas, menores_estrelas = exibir_maiores_menores('Estrelas')

# 2. 5 maiores e 5 menores em tamanho (LOC)
maiores_tamanho, menores_tamanho = exibir_maiores_menores('Tamanho (LOC)')

# 3. 5 maiores e 5 menores em LOC + Comentários
df['LOC + Comentários'] = df['Tamanho (LOC)'] + df['Comentários']
maiores_loc_coment, menores_loc_coment = exibir_maiores_menores('LOC + Comentários')

# 4. 5 maiores e 5 menores em idade (Maturidade)
maiores_idade, menores_idade = exibir_maiores_menores('Maturidade (anos)')

# 5. 5 maiores e menores em Releases
maiores_releases, menores_releases = exibir_maiores_menores('Releases')

# Exibir os resultados
print("Maiores e menores em estrelas:")
print(maiores_estrelas)
print(menores_estrelas)

print("\nMaiores e menores em tamanho (LOC):")
print(maiores_tamanho)
print(menores_tamanho)

print("\nMaiores e menores em LOC + Comentários:")
print(maiores_loc_coment)
print(menores_loc_coment)

print("\nMaiores e menores em idade (Maturidade):")
print(maiores_idade)
print(menores_idade)

print("\nMaiores e menores em Releases:")
print(maiores_releases)
print(menores_releases)
