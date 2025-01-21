import os
from docx import Document

def extract_text_from_docx(file_path):
    """
    Função para extrair texto de um arquivo .docx
    """
    try:
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")
        return None

def process_docx_folder(input_folder, output_folder):
    """
    Processa todos os arquivos .docx na pasta especificada e salva o texto em arquivos .txt
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".docx"):
            file_path = os.path.join(input_folder, file_name)
            print(f"Processando: {file_path}")
            text = extract_text_from_docx(file_path)
            if text:
                output_file_name = f"{os.path.splitext(file_name)[0]}.txt"
                output_file_path = os.path.join(output_folder, output_file_name)
                with open(output_file_path, "w", encoding="utf-8") as output_file:
                    output_file.write(text)
                print(f"Texto extraído e salvo em: {output_file_path}")

def main():
    input_folder = input("Digite o caminho da pasta com os arquivos .docx: ").strip()
    output_folder = os.path.join(os.path.dirname(input_folder), "output")
    
    if not os.path.exists(input_folder):
        print("A pasta especificada não existe.")
        return

    print(f"Iniciando processamento de arquivos .docx na pasta: {input_folder}")
    process_docx_folder(input_folder, output_folder)
    print(f"Processamento concluído. Arquivos salvos em: {output_folder}")

if __name__ == "__main__":
    main()
