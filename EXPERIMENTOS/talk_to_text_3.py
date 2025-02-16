import pyaudio
import wave
import threading
import speech_recognition as sr
import os
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb

# Configurações globais
AUDIO_FILENAME = "recorded_audio.wav"
RECORDING = False

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
        data = stream.read(CHUNK)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    with wave.open(AUDIO_FILENAME, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))

    print(f"Áudio salvo em {AUDIO_FILENAME}")  # Confirmação visual

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

    # Aguarda até que o arquivo esteja disponível
    import time
    time.sleep(1)  # Pequeno atraso para garantir que a gravação finalize

    status_label.config(text="Processando áudio...", foreground="blue")
    threading.Thread(target=transcribe_audio, daemon=True).start()

def transcribe_audio():
    recognizer = sr.Recognizer()
    
    if not os.path.exists(AUDIO_FILENAME):
        text_output.insert(tk.END, "\nErro: O arquivo de áudio não foi encontrado.")
        status_label.config(text="Erro na transcrição", foreground="red")
        return

    try:
        with sr.AudioFile(AUDIO_FILENAME) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="pt-PT")
            text_output.insert(tk.END, f"\n{text}")
            status_label.config(text="Transcrição concluída", foreground="green")
    except Exception as e:
        text_output.insert(tk.END, f"\nErro: {str(e)}")
        status_label.config(text="Erro na transcrição", foreground="red")

# Criar interface gráfica
app = tb.Window(themename="darkly")
app.title("Gravador e Transcritor de Áudio")
app.geometry("500x400")

frame = ttk.Frame(app, padding=20)
frame.pack(fill="both", expand=True)

status_label = ttk.Label(frame, text="Clique para gravar", font=("Arial", 12))
status_label.pack(pady=10)

record_button = ttk.Button(frame, text="Iniciar Gravação", command=start_recording)
record_button.pack(pady=10)

text_output = tk.Text(frame, wrap="word", height=10, font=("Arial", 12))
text_output.pack(fill="both", expand=True, pady=10)

app.mainloop()
