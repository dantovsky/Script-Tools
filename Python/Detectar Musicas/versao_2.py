from pydub import AudioSegment, silence

# Carregar o ficheiro MP3
audio = AudioSegment.from_mp3("Portugal das Maravilhas 02 finalizado.mp3")

# Detectar silêncios maiores que 2 segundos com volume abaixo de -45 dBFS
silences = silence.detect_silence(audio, min_silence_len=2000, silence_thresh=-45)

# Converter milissegundos para mm:ss
def format_time(ms):
    s = ms // 1000
    return f"{s//60:02d}:{s%60:02d}"

# Mostrar os tempos onde cada nova música provavelmente começa
print("Transições prováveis entre músicas:")
for i, (start, end) in enumerate(silences):
    print(f"Música {i+1} começa em: {format_time(end)}")
