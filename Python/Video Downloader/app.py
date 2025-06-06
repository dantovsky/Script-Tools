import os
import sys
import subprocess
import requests
import json
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


def find_videos(page_url):
    """
    Tenta encontrar URLs de vídeos HTML5 na página via requests + BeautifulSoup.
    """
    if page_url.startswith('file://'):
        # ler ficheiro local
        path = page_url[7:]
        try:
            text = open(path, 'r', encoding='utf-8').read()
        except Exception as e:
            print(f"Erro a ler ficheiro local: {e}")
            return []
        soup = BeautifulSoup(text, "html.parser")
    else:
        try:
            resp = requests.get(page_url)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
        except requests.RequestException as e:
            print(f"Erro ao acessar a página: {e}")
            return []

    videos = []
    for video in soup.find_all('video'):
        src = video.get('src') or video.get('data-src')
        if src:
            videos.append(urljoin(page_url, src))
        for source in video.find_all('source'):
            s = source.get('src')
            if s:
                videos.append(urljoin(page_url, s))

    return list(dict.fromkeys(videos))


def extract_videos_selenium(page_url, wait=5):
    """
    Usa Selenium + CDP para interceptar requests de vídeo.
    Retorna URLs .mp4/.webm encontrados.
    """
    if webdriver is None:
        print("Selenium não instalado. Ignorando esta opção.")
        return []

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    # ativa logs de performance
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    videos = []
    try:
        driver.execute_cdp_cmd('Network.enable', {})
        driver.get(page_url)
        driver.implicitly_wait(wait)
        # recolher logs de rede
        logs = driver.get_log('performance')
        for entry in logs:
            msg = json.loads(entry['message'])['message']
            # requestWillBeSent ou responseReceived
            params = msg.get('params', {})
            url = ''
            if msg.get('method') == 'Network.requestWillBeSent':
                url = params.get('request', {}).get('url', '')
            elif msg.get('method') == 'Network.responseReceived':
                url = params.get('response', {}).get('url', '')
            if isinstance(url, str) and url.lower().endswith(('.mp4', '.webm', '.mov')):
                videos.append(url)
    except Exception as e:
        print(f"Erro Selenium/CDP: {e}")
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
                    if chunk:
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
    page_url = input("Insere o URL da página ou file://caminho: ")
    vids = find_videos(page_url)

    if not vids:
        print("Nenhum vídeo HTML5 encontrado via requests.")
        if webdriver:
            try_sel = input("Tentar via Selenium/CDP? (y/n): ")
            if try_sel.lower() == 'y':
                vids = extract_videos_selenium(page_url)
        if not vids:
            print("Nenhum vídeo encontrado via Selenium/CDP.")
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
