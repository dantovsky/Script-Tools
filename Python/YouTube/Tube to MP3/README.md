# Tube to MP3 | Conversor de Vídeos do YouTube para arquivos de áudio (mp3)

## O programa pode ser executado com o comando:
```
python tube_do_mp3.py
```

## Programa que faz o build e gera um executável:
Como alternativa pode ser gerado um executável para utilizar em computadores que não tenham o Python instalado e nem as libs necessárias.
```
pip install cx_Freeze moviepy
```

## Foi criado o ficheiro `setup.py` com o conteúdo:
```py
import sys
from cx_Freeze import setup, Executable

# Dependências adicionais
build_exe_options = {
    "packages": ["os", "yt_dlp", "moviepy.editor", "tkinter", "re", "threading"],
    "includes": [],
    "excludes": [],
    "include_files": []
}

# Definição do executável
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Para evitar a janela do console, use "Win32GUI"

setup(
    name="tube_to_mp3",
    version="1.0",
    description="YouTube to MP3 Downloader",
    options={"build_exe": build_exe_options},
    executables=[Executable("tube_to_mp3.py", base=base)]
)
```

## Depois corrido o comando para gerar o build:
```
python setup.py build

```

## Links +uteis

01. É legal baixar vídeos do YouTube? Regra de 2024
    https://www.dumpmedia.com/pt/video-converter/is-it-legal-to-download-youtube-videos.html
