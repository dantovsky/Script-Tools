import os
import sys
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# Instalação de dependências
# pip install requests bs4

def find_videos(page_url):
    try:
        resp = requests.get(page_url)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao acessar a página: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    videos = []

    # procura tags <video src>
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
    local_filename = os.path.basename(urlparse(video_url).path)
    if not local_filename:
        local_filename = 'downloaded_video'
    print(f"A descarregar {video_url} ...")
    try:
        with requests.get(video_url, stream=True) as r:
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))
            with open(local_filename, 'wb') as f:
                downloaded = 0
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total:
                            percent = downloaded * 100 // total
                            sys.stdout.write(f"\r{percent}%")
                            sys.stdout.flush()
        print(f"\nDescarregado para: {local_filename}")
    except requests.RequestException as e:
        print(f"Erro ao descarregar o vídeo: {e}")

if __name__ == '__main__':
    url = input("Insere o link da página: ")
    vids = find_videos(url)
    if not vids:
        print("Nenhum vídeo HTML5 encontrado nesta página.")
        sys.exit(0)

    print("Vídeos encontrados:")
    for i, v in enumerate(vids, 1):
        print(f"{i}: {v}")

    choice = input("Escolhe o número do vídeo para descarregar (ou 'q' para sair): ")
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
