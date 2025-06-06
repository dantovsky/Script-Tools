from pydub import AudioSegment
audio = AudioSegment.from_mp3("Portugal das Maravilhas 02 finalizado.mp3")
print("Duração:", len(audio) / 1000, "segundos")
