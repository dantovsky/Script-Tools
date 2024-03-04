import tkinter as tk
from tkinter import simpledialog
import os

# Função para buscar pastas que correspondem ao padrão
def buscar_pastas(pasta_raiz, padrao):
    pastas_correspondentes = [d for d in os.listdir(pasta_raiz) if padrao in d and os.path.isdir(os.path.join(pasta_raiz, d))]
    return pastas_correspondentes

# Função principal
def main():
    # Cria uma janela de diálogo para entrada do usuário
    root = tk.Tk()
    root.withdraw() # Esconde a janela principal do Tkinter
    padrao = simpledialog.askstring("Padrão de Pesquisa", "Informe o padrão de busca:")

    if padrao:
        pasta_raiz = os.getcwd() # Ou defina sua pasta raiz específica
        pastas = buscar_pastas(pasta_raiz, padrao)
        print(f"Pastas encontradas: {pastas}")
    else:
        print("Nenhum padrão fornecido.")

if __name__ == "__main__":
    main()
