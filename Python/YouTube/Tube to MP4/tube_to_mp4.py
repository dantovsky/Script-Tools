import os
import yt_dlp
import re
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def open_output_folder():
    output_folder = os.path.join(os.getcwd(), "Videos Convertidos")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    subprocess.Popen(f'explorer "{output_folder}"')

def download_youtube_video(url, quality, progress_var, progress_bar):
    output_folder = os.path.join(os.getcwd(), "Videos Convertidos")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    ydl_opts = {
        'format': f'bestvideo[height<={quality}]+bestaudio/best[ext=mp4]/best[ext=mp4]',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'progress_hooks': [lambda d: update_progress_bar(d['_percent_str'], progress_var, progress_bar)],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = sanitize_filename(info_dict.get('title', None))
            filename = f"{title}.mp4"
        
        messagebox.showinfo("Download Completo", f"Download concluído: {filename}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

def update_progress_bar(status, progress_var, progress_bar):
    match = re.search(r'(\d+(\.\d+)?%)', status)
    if match:
        progress = float(match.group(1).replace('%', ''))
        progress_var.set(progress)
        progress_bar['value'] = progress

def start_download():
    url = url_entry.get()
    quality = quality_var.get()
    if not url:
        messagebox.showwarning("Erro", "Por favor, insira a URL do YouTube.")
    elif not quality:
        messagebox.showwarning("Erro", "Por favor, escolha a qualidade do vídeo.")
    else:
        threading.Thread(target=download_youtube_video, args=(url, quality, progress_var, progress_bar)).start()

# Criando a interface gráfica
root = tk.Tk()
root.title("YouTube Video Downloader ♥ For Rita my LOVE")

# Adicionando padding usando um frame
padding_frame = ttk.Frame(root, padding="40 20")
padding_frame.pack(fill='both', expand=True)

# Estilo personalizado para Entry
style = ttk.Style()
style.configure("TEntry", padding=(10, 10, 10, 10), relief="flat")

# URL do YouTube
url_label = tk.Label(padding_frame, text="URL do YouTube:", anchor="w")
url_label.pack(pady=5, fill='x')
url_entry = ttk.Entry(padding_frame, width=75, style="TEntry")
url_entry.pack(pady=5)

# Opções de Qualidade
quality_label = tk.Label(padding_frame, text="Escolha a qualidade do vídeo:", anchor="w")
quality_label.pack(pady=5, fill='x')
quality_var = tk.StringVar(value="720")  # Define 720p como padrão
quality_options = [("1080p", "1080"), ("720p", "720"), ("480p", "480"), ("360p", "360")]
for text, value in quality_options:
    ttk.Radiobutton(padding_frame, text=text, variable=quality_var, value=value).pack(anchor=tk.W)

# Botão para iniciar o download
tk.Button(padding_frame, text="Download", command=start_download).pack(pady=20)

# Link para abrir a pasta de destino
link_button = tk.Button(padding_frame, text="Ir para a pasta dos vídeos", command=open_output_folder, fg="blue", cursor="hand2")
link_button.pack(pady=10)

# Barra de progresso
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(padding_frame, variable=progress_var, maximum=100)
progress_bar.pack(pady=10, fill='x')

# Iniciando o loop da interface
root.mainloop()
