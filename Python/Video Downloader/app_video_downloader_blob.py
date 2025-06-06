import os
import sys
import subprocess
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# Instalação de dependências
# pip install requests bs4 yt-dlp

def find_videos(page_url):
    """
    Tenta encontrar URLs de vídeos HTML5 na página.
    Retorna lista de src de <video> e <source>.
    """
    try:
        resp = requests.get(page_url)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao acessar a página: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    videos = []

    # procura <video src>
    for video in soup.find_all('video'):
        src = video.get('src')
        if src:
            videos.append(urljoin(page_url, src))
        # procura <source> dentro de <video>
        for source in video.find_all('source'):
            src2 = source.get('src')
            if src2:
                videos.append(urljoin(page_url, src2))

    # remove duplicados
    return list(dict.fromkeys(videos))


def download_video(video_url):
    """
    Descarrega o vídeo por HTTP e mostra progresso.
    """
    filename = os.path.basename(urlparse(video_url).path) or 'video_download'
    print(f"A descarregar {video_url} para {filename}...")
    try:
        with requests.get(video_url, stream=True) as r:
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))
            downloaded = 0
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        pct = downloaded * 100 // total
                        sys.stdout.write(f"\r{pct}%")
                        sys.stdout.flush()
        print(f"\nDescarregado com sucesso: {filename}")
    except requests.RequestException as e:
        print(f"Erro ao descarregar: {e}")


def download_with_ytdlp(page_url):
    """
    Tenta usar yt-dlp para descarregar vídeo(s) da página.
    É necessário ter yt-dlp instalado.
    """
    print("A usar yt-dlp para descarregar vídeo(s)...\n")
    result = subprocess.run(["yt-dlp", page_url])
    if result.returncode == 0:
        print("Descarregamento via yt-dlp concluído.")
    else:
        print("Falha ao usar yt-dlp. Verifique se está instalado e tente novamente.")


if __name__ == '__main__':
    page_url = input("Insere o URL da página: ")
    vids = find_videos(page_url)

    if vids:
        print("\nVídeos HTML5 encontrados:")
        for i, v in enumerate(vids, 1):
            print(f"{i}: {v}")
        choice = input("Escolhe o número para descarregar ou 'q' para sair: ")
        if choice.lower() == 'q':
            sys.exit(0)
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(vids):
                download_video(vids[idx])
            else:
                print("Escolha inválida.")
        except ValueError:
            print("Entrada inválida.")
    else:
        print("\nNão foram encontrados vídeos HTML5 nesta página.")
        use_ytdlp = input("Desejas tentar com yt-dlp? (y/n): ")
        if use_ytdlp.lower() == 'y':
            download_with_ytdlp(page_url)
        else:
            print("Nenhuma ação adicional. Fim.")
