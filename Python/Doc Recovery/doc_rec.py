import os
from docx import Document
from olefile import OleFileIO
from tkinter import Tk, filedialog, messagebox

def extract_text_from_docx(file_path):
    """Tenta recuperar o texto de um arquivo DOCX."""
    try:
        doc = Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        return f"Erro ao processar DOCX: {e}"

def extract_text_from_doc(file_path):
    """Tenta recuperar o texto de um arquivo DOC (binário)."""
    try:
        if not OleFileIO.isOleFile(file_path):
            return "O arquivo DOC fornecido não é válido ou está corrompido."
        
        ole = OleFileIO(file_path)
        if 'WordDocument' in ole.listdir():
            stream = ole.openstream('WordDocument')
            return stream.read().decode(errors="ignore")  # Recupera texto bruto
        else:
            return "Estrutura do arquivo não contém 'WordDocument'. O arquivo pode estar muito danificado."
    except Exception as e:
        return f"Erro ao processar DOC: {e}"

def save_extracted_text(output_text, output_path):
    """Salva o texto extraído em um arquivo TXT."""
    try:
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(output_text)
        return True
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")
        return False

def main():
    """Interface gráfica para selecionar arquivos e recuperar texto."""
    Tk().withdraw()  # Oculta a janela principal do Tkinter
    file_path = filedialog.askopenfilename(title="Selecione o arquivo DOC ou DOCX", 
                                           filetypes=[("Word Documents", "*.docx *.doc")])
    if not file_path:
        messagebox.showinfo("Cancelado", "Nenhum arquivo selecionado.")
        return
    
    if file_path.endswith(".docx"):
        extracted_text = extract_text_from_docx(file_path)
    elif file_path.endswith(".doc"):
        extracted_text = extract_text_from_doc(file_path)
    else:
        messagebox.showerror("Erro", "O formato do arquivo não é suportado.")
        return

    # Mostrar um resumo ao usuário
    print("\nTexto Extraído (Resumo):")
    print(extracted_text[:500])  # Limite inicial para exibição no terminal

    # Perguntar onde salvar o arquivo recuperado
    save_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")],
                                             title="Salvar o texto recuperado como")
    if save_path:
        if save_extracted_text(extracted_text, save_path):
            messagebox.showinfo("Sucesso", f"Texto salvo com sucesso em:\n{save_path}")
        else:
            messagebox.showerror("Erro", "Erro ao salvar o arquivo de texto.")
    else:
        messagebox.showinfo("Cancelado", "Nenhum local selecionado para salvar o texto.")

if __name__ == "__main__":
    main()
