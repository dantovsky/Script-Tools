import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
import threading
import os

# Configuração global
AUDIO_FILE = "recorded_audio.wav"
SAMPLERATE = 44100  # Taxa de amostragem
DURATION = 10  # Duração máxima da gravação (em segundos)
recording = False  # Flag para indicar se está gravando

def record_audio():
    """Inicia a gravação do áudio."""
    global recording
    recording = True
    messagebox.showinfo("Gravação", "Iniciando gravação. Fale agora!")
    
    audio_data = []

    def callback(indata, frames, time, status):
        """Função chamada em cada bloco de áudio capturado."""
        if status:
            print(status)
        if recording:
            audio_data.append(indata.copy())

    with sd.InputStream(samplerate=SAMPLERATE, channels=1, callback=callback):
        sd.sleep(DURATION * 1000)  # Tempo de gravação em milissegundos
    
    recording = False
    audio_array = np.concatenate(audio_data, axis=0)
    wav.write(AUDIO_FILE, SAMPLERATE, (audio_array * 32767).astype(np.int16))
    messagebox.showinfo("Gravação", "Gravação finalizada!")

def stop_recording():
    """Para a gravação do áudio."""
    global recording
    recording = False

def transcribe_audio():
    """Transcreve o áudio gravado para texto."""
    if not os.path.exists(AUDIO_FILE):
        messagebox.showerror("Erro", "Nenhum áudio gravado encontrado.")
        return

    recognizer = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio_data = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio_data, language="pt-PT")
        messagebox.showinfo("Transcrição", f"Texto reconhecido:\n\n{text}")
    except sr.UnknownValueError:
        messagebox.showwarning("Transcrição", "Não foi possível reconhecer o áudio.")
    except sr.RequestError:
        messagebox.showerror("Erro", "Erro ao acessar o serviço de reconhecimento de voz.")

# Criar a interface gráfica
app = tb.Window(themename="superhero")
app.title("Gravador de Áudio e Transcrição")
app.geometry("400x300")

frame = ttk.Frame(app, padding="20")
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Gravador de Áudio", font=("Arial", 16)).pack(pady=10)

record_btn = ttk.Button(frame, text="🎤 Iniciar Gravação", command=lambda: threading.Thread(target=record_audio).start())
record_btn.pack(pady=5)

stop_btn = ttk.Button(frame, text="⏹️ Parar Gravação", command=stop_recording)
stop_btn.pack(pady=5)

transcribe_btn = ttk.Button(frame, text="📝 Transcrever Áudio", command=transcribe_audio)
transcribe_btn.pack(pady=5)

app.mainloop()
