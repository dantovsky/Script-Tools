from pydub import AudioSegment, silence
import matplotlib.pyplot as plt

# pip install pydub pyaudioop matplotlib

# Caminho para o teu ficheiro MP3
audio = AudioSegment.from_mp3("Portugal das Maravilhas 02 finalizado.mp3")

# Detectar silencios maiores que 2 segundos abaixo de -45 dBFS
silences = silence.detect_silence(audio, min_silence_len=2000, silence_thresh=-45)

# Converter ms para mm:ss
def format_time(ms):
    s = ms // 1000
    return f"{s//60:02d}:{s%60:02d}"

print("Transições prováveis entre músicas:")
for i, (start, end) in enumerate(silences):
    print(f"Música {i+1} começa em: {format_time(end)}")

# (Opcional) Mostrar gráfico de silêncio
volumes = [segment.dBFS for segment in audio[::1000]]
plt.plot(volumes)
plt.title("Volume ao longo do tempo")
plt.xlabel("Segundos")
plt.ylabel("dBFS")
plt.grid()
plt.show()
