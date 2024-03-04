import tkinter as tk
from tkinter import simpledialog, Toplevel, Label, Entry, Button, Radiobutton, StringVar

def buscar_e_substituir(padrao, substituto=None, remover=False):
    print(f"Padrão: {padrao}, Substituto: {substituto}, Remover: {remover}")
    # Aqui vai a lógica para buscar nas pastas e substituir ou remover conforme a escolha

def dialogo_avancado():
    def ok_action():
        padrao = entry.get()
        substituto = substituto_entry.get() if substituto_var.get() else None
        buscar_e_substituir(padrao, substituto, remover=acao_var.get() == 'remover')
        dialogo.destroy()

    dialogo = Toplevel()
    dialogo.geometry("400x200")
    
    Label(dialogo, text="Informe o padrão de busca:").pack()
    entry = Entry(dialogo)
    entry.pack()
    
    acao_var = StringVar(value="remover")
    Radiobutton(dialogo, text="Remover após padrão", variable=acao_var, value='remover').pack()
    Radiobutton(dialogo, text="Substituir padrão", variable=acao_var, value='substituir').pack()
    
    substituto_var = StringVar()
    Label(dialogo, text="Termo de substituição:").pack()
    substituto_entry = Entry(dialogo, textvariable=substituto_var)
    substituto_entry.pack()
    
    Button(dialogo, text="OK", command=ok_action).pack()

root = tk.Tk()
root.withdraw()  # Esconde a janela principal do Tkinter
dialogo_avancado()
root.mainloop()
