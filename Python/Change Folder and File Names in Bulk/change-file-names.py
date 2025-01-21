import tkinter as tk
from tkinter import simpledialog, Toplevel, Label, Entry, Button, Radiobutton, StringVar, Frame, messagebox, Checkbutton, BooleanVar
import os

# Author: Dante Marinho
# App Name: Change Folder and File Names in Bulk
# Description: Utility made with help from ChatGPT v4. This script helps change a mathing term in a list of files and folder in a same root folder. You can change for another term or remove all text from mathing term.

def buscar_e_substituir(padrao, substituto=None, remover=False, pasta_raiz='.', incluir_pastas=True, incluir_ficheiros=True):
    changed_folder = 0
    changed_files = 0

    for item in os.listdir(pasta_raiz):
        caminho_completo = os.path.join(pasta_raiz, item)
        if os.path.isdir(caminho_completo) and incluir_pastas and padrao in item:
            # Processa pastas
            novo_nome = item.replace(padrao, substituto) if not remover else item.split(padrao)[0]
            os.rename(caminho_completo, os.path.join(pasta_raiz, novo_nome))
            changed_folder += 1
        elif os.path.isfile(caminho_completo) and incluir_ficheiros and padrao in item:
            # Processa ficheiros
            nome_base, extensao = os.path.splitext(item)
            novo_nome_base = nome_base.replace(padrao, substituto) if not remover else nome_base.split(padrao)[0]
            novo_nome = novo_nome_base + extensao
            os.rename(caminho_completo, os.path.join(pasta_raiz, novo_nome))
            changed_files += 1

    if changed_folder == 0 and changed_files == 0:
        messagebox.showinfo("Resultado", "Nenhum item correspondente encontrado.")
    else:
        messagebox.showinfo("Resultado", f"{changed_folder} pastas e {changed_files} ficheiros foram alterados.")

def dialogo_avancado():
    pastas_var = BooleanVar(value=True)
    ficheiros_var = BooleanVar(value=True)

    def ok_action():
        padrao = entry.get()

        if not padrao: # return if None or empty string
            return

        incluir_pastas = pastas_var.get()
        incluir_ficheiros = ficheiros_var.get()
        substituto = substituto_entry.get() if acao_var.get() == 'substituir' else None
        buscar_e_substituir(padrao, substituto, remover=acao_var.get() == 'remover', incluir_pastas=incluir_pastas, incluir_ficheiros=incluir_ficheiros)
        # dialogo.destroy()

    spacing = 12

    dialogo = Toplevel()
    dialogo.title("Change Folder and File Names in Bulk")
    dialogo.geometry("400x285")
    frame = Frame(dialogo)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    Label(frame, text="Informe o padrão de busca:", anchor='w', justify='left', width=80).pack()
    entry = Entry(frame, font=('Ubuntu', 12, 'bold'))
    entry.pack(anchor='w', fill=tk.X)
    entry.bind("<Return>", lambda event=None: ok_action())

    tk.Frame(frame, height=spacing).pack()
    acao_var = StringVar(value="remover")
    Radiobutton(frame, text="Remover após padrão", variable=acao_var, value='remover', anchor='w', justify='left', width=80).pack()
    Radiobutton(frame, text="Substituir padrão", variable=acao_var, value='substituir', anchor='w', justify='left', width=80).pack()

    tk.Frame(frame, height=spacing).pack()
    Label(frame, text="Termo de substituição:", anchor='w', justify='left', width=80).pack()
    substituto_var = StringVar()
    substituto_entry = Entry(frame, textvariable=substituto_var, font=('Ubuntu', 12, 'bold'))
    substituto_entry.pack(anchor='w', fill=tk.X)
    substituto_entry.bind("<Return>", lambda event=None: ok_action())

    tk.Frame(frame, height=spacing).pack()
    Checkbutton(frame, text="Pastas", variable=pastas_var, anchor='w', justify='left', width=80).pack()
    Checkbutton(frame, text="Ficheiros", variable=ficheiros_var, anchor='w', justify='left', width=80).pack()

    tk.Frame(frame, height=spacing).pack()
    ok_button = Button(frame, text="OK", command=ok_action, bg='#332299', fg='white', pady=8)
    ok_button.pack(anchor='w', fill=tk.X)


    dialogo.protocol("WM_DELETE_WINDOW", on_closing)  # Adiciona o manipulador de evento

def on_closing():
    root.destroy()  # Destrói a janela principal
    root.quit()     # Encerra o loop principal do Tkinter

root = tk.Tk()
root.withdraw()
dialogo_avancado()
root.mainloop()
