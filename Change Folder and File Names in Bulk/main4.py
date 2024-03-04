import tkinter as tk
from tkinter import simpledialog, Toplevel, Label, Entry, Button, Radiobutton, StringVar, Frame, messagebox
import os

def buscar_e_substituir(padrao, substituto=None, remover=False, pasta_raiz='.'):
    pastas_alteradas = 0
    for pasta in os.listdir(pasta_raiz):
        caminho_completo = os.path.join(pasta_raiz, pasta)
        if os.path.isdir(caminho_completo) and padrao in pasta:
            if remover:
                novo_nome = pasta.split(padrao)[0]
            else:
                novo_nome = pasta.replace(padrao, substituto if substituto else '')
            os.rename(caminho_completo, os.path.join(pasta_raiz, novo_nome))
            pastas_alteradas += 1
    if pastas_alteradas == 0:
        messagebox.showinfo("Resultado", "Nenhuma pasta correspondente encontrada.")
        # buscar_e_substituir(padrao, substituto, remover, pasta_raiz)
    else:
        messagebox.showinfo("Resultado", f"{pastas_alteradas} pastas foram alteradas.")

def dialogo_avancado():
    def ok_action():
        padrao = entry.get()

        if not padrao:
            return

        substituto = substituto_entry.get() if acao_var.get() == 'substituir' else None
        buscar_e_substituir(padrao, substituto, remover=acao_var.get() == 'remover')
        # dialogo.destroy()

    dialogo = Toplevel()
    dialogo.title("Change Folder Names in Bulk")
    dialogo.geometry("400x200")
    frame = Frame(dialogo)
    frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    Label(frame, text="Informe o padrão de busca:").pack(anchor='w', fill=tk.X)
    entry = Entry(frame)
    entry.pack(anchor='w', fill=tk.X)
    entry.bind("<Return>", lambda event=None: ok_action())

    acao_var = StringVar(value="remover")
    Radiobutton(frame, text="Remover após padrão", variable=acao_var, value='remover').pack(anchor='w', fill=tk.X)
    Radiobutton(frame, text="Substituir padrão", variable=acao_var, value='substituir').pack(anchor='w', fill=tk.X)

    Label(frame, text="Termo de substituição:").pack(anchor='w', fill=tk.X)
    substituto_var = StringVar()
    substituto_entry = Entry(frame, textvariable=substituto_var)
    substituto_entry.pack(anchor='w', fill=tk.X)
    substituto_entry.bind("<Return>", lambda event=None: ok_action())

    Button(frame, text="OK", command=ok_action).pack(anchor='w', fill=tk.X)

    dialogo.protocol("WM_DELETE_WINDOW", on_closing)  # Adiciona o manipulador de evento

def on_closing():
    root.destroy()  # Encerra a aplicação

root = tk.Tk()
root.withdraw()
dialogo_avancado()
root.mainloop()
