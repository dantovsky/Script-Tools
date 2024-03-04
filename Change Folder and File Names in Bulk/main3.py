import tkinter as tk
from tkinter import simpledialog, Toplevel, Label, Entry, Button, Radiobutton, StringVar, Frame
import os

def buscar_e_substituir(padrao, substituto=None, remover=False, pasta_raiz='.'):
    for pasta in os.listdir(pasta_raiz):
        caminho_completo = os.path.join(pasta_raiz, pasta)
        if os.path.isdir(caminho_completo) and padrao in pasta:
            if remover:
                novo_nome = pasta.split(padrao)[0]
            else:
                novo_nome = pasta.replace(padrao, substituto if substituto else '')
            os.rename(caminho_completo, os.path.join(pasta_raiz, novo_nome))
            print(f"Renomeada: {pasta} para {novo_nome}")

def dialogo_avancado():
    def ok_action():
        padrao = entry.get()
        substituto = substituto_entry.get() if acao_var.get() == 'substituir' else None
        buscar_e_substituir(padrao, substituto, remover=acao_var.get() == 'remover')
        dialogo.destroy()

    dialogo = Toplevel()
    dialogo.geometry("400x200")
    frame = Frame(dialogo)
    frame.pack(side=tk.LEFT, anchor=tk.N, padx=10, pady=10)

    Label(frame, text="Informe o padrão de busca:").pack(anchor='w')
    entry = Entry(frame)
    entry.pack(anchor='w')

    acao_var = StringVar(value="remover")
    Radiobutton(frame, text="Remover após padrão", variable=acao_var, value='remover').pack(anchor='w')
    Radiobutton(frame, text="Substituir padrão", variable=acao_var, value='substituir').pack(anchor='w')

    Label(frame, text="Termo de substituição:").pack(anchor='w')
    substituto_var = StringVar()
    substituto_entry = Entry(frame, textvariable=substituto_var)
    substituto_entry.pack(anchor='w')

    Button(frame, text="OK", command=ok_action).pack(anchor='w')

root = tk.Tk()
root.withdraw()
dialogo_avancado()
root.mainloop()
