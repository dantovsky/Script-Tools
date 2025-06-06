import os
import sys
import subprocess
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    webdriver = None

# Instalação de dependências
# pip install requests bs4 selenium webdriver-manager yt-dlp

def find_videos(page_url):
    """
    Tenta encontrar URLs de vídeos HTML5 na página via requests + BeautifulSoup.
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

    for video in soup.find_all('video'):
        src = video.get('src') or video.get('data-src')
        if src:
            videos.append(urljoin(page_url, src))
        for source in video.find_all('source'):
            src2 = source.get('src')
            if src2:
                videos.append(urljoin(page_url, src2))

    return list(dict.fromkeys(videos))


def extract_videos_selenium(page_url, wait=5):
    """
    Usa Selenium para carregar a página e extrair src atuais de <video>, incluindo blobs.
    Requer 'selenium' e 'webdriver-manager'.
    """
    if webdriver is None:
        print("Selenium não instalado. Ignorando esta opção.")
        return []

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")

    # Inicializa Chrome driver com Service
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    videos = []
    try:
        driver.get(page_url)
        driver.implicitly_wait(wait)
        elems = driver.find_elements(By.TAG_NAME, "video")
        for el in elems:
            src = el.get_attribute('currentSrc') or el.get_attribute('src')
            if src:
                videos.append(src)
    except Exception as e:
        print(f"Erro Selenium: {e}")
    finally:
        driver.quit()

    return list(dict.fromkeys(videos))


def download_video(video_url):
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
        print(f"\nDescarregado: {filename}")
    except requests.RequestException as e:
        print(f"Erro ao descarregar: {e}")


def download_with_ytdlp(page_url):
    print("A usar yt-dlp para descarregar vídeo(s)...")
    res = subprocess.run(["yt-dlp", page_url])
    if res.returncode == 0:
        print("yt-dlp concluiu o descarregamento.")
    else:
        print("Erro yt-dlp. Verifica instalação e URL.")


if __name__ == '__main__':
    page_url = input("Insere o URL da página: ")
    vids = find_videos(page_url)

    if not vids:
        print("Nenhum vídeo HTML5 encontrado via requests.")
        try_sel = input("Tentar via Selenium? (y/n): ")
        if try_sel.lower() == 'y':
            vids = extract_videos_selenium(page_url)
        if not vids:
            print("Nenhum vídeo via Selenium.")
            use_ytdlp = input("Tentar com yt-dlp? (y/n): ")
            if use_ytdlp.lower() == 'y':
                download_with_ytdlp(page_url)
            else:
                print("Fim.")
            sys.exit(0)

    print("\nVídeos encontrados:")
    for i, v in enumerate(vids, 1):
        print(f"{i}: {v}")
    choice = input("Escolhe número para descarregar ou 'q' para sair: ")
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
