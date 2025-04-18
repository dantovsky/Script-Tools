import os
import threading
import subprocess
import wave
import pyaudio
import whisper
import tkinter as tk
from tkinter import ttk, filedialog
import ttkbootstrap as tb

# Talk to Text v5
# Versão com pontuações e que recebe os tipos de input:
# » ficheiro de áudio
# » ficheiro de vídeo 
# » gravação de áudio em tempo real

# Instalação de dependências
# pip install pyaudio whisper ttkbootstrap
# Se o whisper der erro, instala direto do Github
# python -m pip install git+https://github.com/openai/whisper.git

# Ficheiro de saída de áudio
AUDIO_FILENAME = "recorded_audio.wav"
RECORDING = False

# Grava áudio do microfone
def record_audio():
    global RECORDING
    RECORDING = True
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []

    while RECORDING:
        frames.append(stream.read(CHUNK))

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Guarda WAV
    with wave.open(AUDIO_FILENAME, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))

    status_label.config(text=f"Áudio salvo: {AUDIO_FILENAME}", foreground="green")
    threading.Thread(target=transcribe_audio, daemon=True).start()

# Inicia/parar gravação
def start_recording():
    global RECORDING
    if not RECORDING:
        threading.Thread(target=record_audio, daemon=True).start()
        status_label.config(text="Gravando...", foreground="red")
        record_button.config(text="Parar Gravação", command=stop_recording)

def stop_recording():
    global RECORDING
    RECORDING = False
    record_button.config(text="Iniciar Gravação", command=start_recording)
    status_label.config(text="A processar gravação...", foreground="blue")

# Processa ficheiro áudio/vídeo
def process_file():
    file_path = filedialog.askopenfilename(
        title="Seleciona ficheiro áudio/vídeo",
        filetypes=[
            ("Áudio/Vídeo comuns", ("*.wav","*.mp3","*.mp4","*.m4a","*.flac","*.avi","*.mov","*.mkv")),
            ("Todos os ficheiros", "*.*"),
        ]
    )
    if not file_path:
        return
    status_label.config(text="A extrair áudio...", foreground="blue")
    cmd = [
        "ffmpeg", "-y", "-i", file_path,
        "-ar", "16000", "-ac", "1", AUDIO_FILENAME
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        status_label.config(text="Áudio extraído", foreground="green")
        threading.Thread(target=transcribe_audio, daemon=True).start()
    except subprocess.CalledProcessError:
        text_output.insert(tk.END, "\nErro: falha ao extrair áudio.")
        status_label.config(text="Erro na extração", foreground="red")

# Transcreve o WAV com Whisper
def transcribe_audio():
    if not os.path.exists(AUDIO_FILENAME):
        text_output.insert(tk.END, "\nErro: áudio não encontrado.")
        status_label.config(text="Erro na transcrição", foreground="red")
        return
    status_label.config(text="A transcrever...", foreground="blue")
    try:
        model = whisper.load_model("base")
        result = model.transcribe(AUDIO_FILENAME)
        text_output.insert(tk.END, f"\n{result['text']}")
        status_label.config(text="Transcrição concluída", foreground="green")
    except Exception as e:
        text_output.insert(tk.END, f"\nErro: {e}")
        status_label.config(text="Erro na transcrição", foreground="red")

# Interface gráfica
app = tb.Window(themename="darkly")
app.title("Gravador e Transcritor de Áudio/Vídeo")
app.geometry("600x500")

frame = ttk.Frame(app, padding=20)
frame.pack(fill="both", expand=True)

status_label = ttk.Label(frame, text="Escolhe gravar ou carregar ficheiro", font=("Arial", 12))
status_label.pack(pady=10)

# Botões
button_frame = ttk.Frame(frame)
button_frame.pack(pady=10)

record_button = ttk.Button(button_frame, text="Iniciar Gravação", command=start_recording)
record_button.grid(row=0, column=0, padx=5)

file_button = ttk.Button(button_frame, text="Carregar Ficheiro", command=process_file)
file_button.grid(row=0, column=1, padx=5)

# Text output
text_output = tk.Text(frame, wrap="word", height=15, font=("Arial", 12))
text_output.pack(fill="both", expand=True, pady=10)

app.mainloop()
