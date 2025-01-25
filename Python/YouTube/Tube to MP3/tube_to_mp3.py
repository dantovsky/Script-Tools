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

def download_youtube_video(url, kbps, progress_var, progress_bar):
    output_folder = os.path.join(os.getcwd(), "Videos Convertidos")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': kbps,
        }],
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'progress_hooks': [lambda d: update_progress_bar(d['_percent_str'], progress_var, progress_bar)]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = sanitize_filename(info_dict.get('title', None))
            filename = f"{title}.mp3"
        
        messagebox.showinfo("Download Completo", f"Downloaded and converted to MP3: {filename}")
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
    kbps = kbps_var.get()
    if not url:
        messagebox.showwarning("Erro", "Por favor, insira a URL do YouTube.")
    elif not kbps:
        messagebox.showwarning("Erro", "Por favor, escolha a taxa de KBPS.")
    else:
        threading.Thread(target=download_youtube_video, args=(url, kbps, progress_var, progress_bar)).start()

# Criando a interface gráfica
root = tk.Tk()
root.title("YouTube to MP3 Downloader ♥ For Rita my LOVE")

# Adicionando padding usando um frame
padding_frame = ttk.Frame(root, padding="40 20")
padding_frame.pack(fill='both', expand=True)

# Estilo personalizado para Entry
style = ttk.Style()
style.configure("TEntry", padding=(10, 10, 10, 10), relief="flat")  # Adicionando padding e removendo a borda

# URL do YouTube
url_label = tk.Label(padding_frame, text="URL do YouTube:", anchor="w")
url_label.pack(pady=5, fill='x')
url_entry = ttk.Entry(padding_frame, width=75, style="TEntry")
url_entry.pack(pady=5)

# Opções de KBPS
kpbs_label = tk.Label(padding_frame, text="Escolha a taxa de KBPS:", anchor="w")
kpbs_label.pack(pady=5, fill='x')
kbps_var = tk.StringVar(value="192")  # Define 192 KBPS como padrão
kbps_options = ["128", "192", "256", "320"]
for kbps in kbps_options:
    ttk.Radiobutton(padding_frame, text=kbps, variable=kbps_var, value=kbps).pack(anchor=tk.W)

# Botão para iniciar o download
tk.Button(padding_frame, text="Download", command=start_download).pack(pady=20)

# Link para abrir a pasta de destino
link_button = tk.Button(padding_frame, text="Ir para a pasta dos áudios", command=open_output_folder, fg="blue", cursor="hand2")
link_button.pack(pady=10)

# Barra de progresso
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(padding_frame, variable=progress_var, maximum=100)
progress_bar.pack(pady=10, fill='x')

# Iniciando o loop da interface
root.mainloop()
