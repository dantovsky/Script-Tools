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
