import pandas as pd

# Criar uma lista com os dados extraídos manualmente do HTML
data = [
    ["João Araújo", "", "joaopontes.araujo@gmail.com"],
    ["Lucas Cordeiro da Silva", "910375830", "cordeiro0620@gmail.com"],
    ["Luis", "919821564", "edu.zonaro@hotmail.com"],
    ["Patricia Costa", "912816703", "pccantocoral@gmail.com"],
    ["Túlio Silva", "925156631", "tuliomarcodasilva@gmail.com"],
    ["Rodrigo", "916604368", "rodrigoayoub@gmail.com"],
    ["Ana", "", "amarkkes@gmail.com"]
]

# Criar um DataFrame
df = pd.DataFrame(data, columns=["Nome", "Telefone", "Email"])

# Salvar como CSV
csv_file_path = "/mnt/data/contatos.csv"
df.to_csv(csv_file_path, index=False, encoding="utf-8")

# Exibir o CSV para o usuário
import ace_tools as tools
tools.display_dataframe_to_user(name="Contatos Extraídos", dataframe=df)

# Retornar o caminho do arquivo CSV
csv_file_path
