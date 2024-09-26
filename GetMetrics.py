import requests
from datetime import datetime
import csv
import json

# Configurações da API
GITHUB_API_URL = "https://api.github.com/graphql"
TOKEN = ""  

headers = {"Authorization": f"Bearer {TOKEN}"}

# Função para executar a consulta GraphQL
def run_query(query, variables={}):
    request = requests.post(GITHUB_API_URL, json={'query': query, 'variables': variables}, headers=headers)
    
    if request.status_code == 200:
        response_json = request.json()
        if 'data' in response_json:
            return response_json
        else:
            print("Erro: 'data' não encontrado na resposta.")
            print("Resposta completa:", json.dumps(response_json, indent=4))  
            raise Exception("A resposta da API não contém 'data'.")
    else:
        print(f"Erro na consulta: Código {request.status_code}")
        print(f"Resposta completa: {request.text}")  
        raise Exception(f"Query failed to run by returning code of {request.status_code}. {query}")

# Consulta GraphQL 
query = """
query ($after: String) {
  search(query: "language:Java stars:>1", type: REPOSITORY, first: 10, after: $after) {
    repositoryCount
    pageInfo {
      endCursor
      hasNextPage
    }
    edges {
      node {
        ... on Repository {
          name
          createdAt
          stargazers {
            totalCount
          }
          releases {
            totalCount
          }
          object(expression: "HEAD:README.md") {
            ... on Blob {
              text
            }
          }
        }
      }
    }
  }
}
"""

variables = {"after": None}
resultados = []
total_repos = 0
max_repos = 1000

while total_repos < max_repos:
    result = run_query(query, variables)
    data = result['data']['search']
    resultados.extend(data['edges'])
    total_repos += len(data['edges'])
    if not data['pageInfo']['hasNextPage'] or total_repos >= max_repos:
        break
    variables['after'] = data['pageInfo']['endCursor']

resultados = resultados[:max_repos]

# Função para calcular o número de linhas e comentários
def calcular_loc(text):
    linhas = text.split('\n')
    loc = sum(1 for linha in linhas if linha.strip() and not linha.strip().startswith('#'))
    comentarios = sum(1 for linha in linhas if linha.strip().startswith('#'))
    return loc, comentarios

# Processar os dados e salvar as informações em um arquivo CSV
with open('DadosRQ.csv', mode='w', newline='') as arquivo_csv:
    writer = csv.writer(arquivo_csv)
    writer.writerow(["Nome do Repositório", "Estrelas", "Tamanho (LOC)", "Comentários", "Releases", "Maturidade (anos)"])
    
    for index, repo in enumerate(resultados, start=1):
        repo_data = repo['node']
        readme_text = repo_data['object']['text'] if repo_data['object'] else ""
        
        # Tamanho: LOC e linhas de comentários
        loc, comentarios = calcular_loc(readme_text)
        
        # Maturidade: diferença entre a data atual e a data de criação
        data_criacao = datetime.strptime(repo_data['createdAt'], "%Y-%m-%dT%H:%M:%SZ")
        idade_anos = (datetime.now() - data_criacao).days / 365
        
        # Popularidade e atividade
        estrelas = repo_data['stargazers']['totalCount']
        releases = repo_data['releases']['totalCount']
        
        writer.writerow([repo_data['name'], estrelas, loc, comentarios, releases, round(idade_anos, 2)])

print("Os dados foram salvos no arquivo 'DadosRQ.csv'.")
