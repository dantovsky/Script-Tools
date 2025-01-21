import os
import requests
from PIL import Image, ExifTags

# Program Name: Download Images From URL List and Compress
# About :: Download images from links, compress and resize
# Author: Dante Marinho and ChatGPT (Portugal)
# Date: 19/12/2023
# Version: 0.1.3

# Configs
destination_folder = ".\images_out" # Pasta de destino para salvar as imagens
base_name = "nome da imagem"
max_horizontal_width = 1400
max_square_width = 1200
max_vertical_width = 700
compression_quality = 72
is_to_compress_and_resize = True # 'False' apenas comprime

# Lista contendo URLs das imagens. Formato: { "url": "https://link-to-image.com/media/image-name.jpg" }
url_image_list = [
    { "url": "https://cdn.pixabay.com/photo/2023/12/13/17/54/bun-8447394_1280.jpg" },
    { "url": "https://cdn.pixabay.com/photo/2019/11/18/19/48/pretzels-4635648_960_720.jpg" },
    { "url": "https://cdn.pixabay.com/photo/2019/11/18/19/48/pretzels-4635649_1280.jpg" },
]

# Garante que a pasta de destino exista
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

def compress_and_resize_image(image_path, output_path):
    try:
        # Abre a imagem
        img = Image.open(image_path)

        # Obtém a orientação da imagem
        orientation = 0
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation]=='Orientation':
                    break
            exif=dict(img._getexif().items())

            if exif[orientation] == 3:
                img=img.rotate(180, expand=True)
            elif exif[orientation] == 6:
                img=img.rotate(270, expand=True)
            elif exif[orientation] == 8:
                img=img.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # A imagem não tem informações de orientação no EXIF
            pass

        # Determina o formato da imagem (horizontal, quadrada ou vertical)
        format_type = "horizontal" if img.width > img.height else "square" if img.width == img.height else "vertical"

        # Define a largura máxima com base no formato da imagem
        max_width = (
            max_horizontal_width if format_type == "horizontal"
            else max_square_width if format_type == "square"
            else max_vertical_width
        )

        # Redimensiona a imagem de acordo com as regras
        if img.width < max_width:
            max_width = img.width

        ratio = max_width / float(img.width)
        new_height = int(float(img.height) * float(ratio))
        img = img.resize((max_width, new_height))

        # Salva a imagem com compressão
        img.save(output_path, optimize=True, quality=compression_quality)

        # print(f"Imagem processada: {output_path}")
        print(f"Imagem baixada, comprimida e resized: {output_path}")

    except Exception as e:
        print(f"Erro ao processar a imagem {image_path}: {e}")

# Loop através das informações das imagens
for i, image_info in enumerate(url_image_list):
    try:
        # Faz o download da imagem
        response = requests.get(image_info["url"])
        response.raise_for_status()

        image_extension = image_info["url"].split(".")[-1]        

        # Obtém o nome do arquivo personalizado
        file_path = os.path.join(destination_folder, (base_name + " " + str(i + 1)) + "." + image_extension) # Outra forma para obter o nome: os.path.basename(image_url)

        # Salva a imagem no disco
        with open(file_path, 'wb') as file:
            file.write(response.content)

        # COMPRESS ?
        if is_to_compress_and_resize:
            compress_and_resize_image(file_path, file_path)
        else:
            # Abre a imagem usando Pillow
            img = Image.open(file_path)

            # Comprime a imagem e guarda
            img.save(file_path, optimize=True, quality=compression_quality)
            print(f"Imagem baixada com quality = {compression_quality}: {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar a imagem {image_info['url']}: {e}")

print("Download de imagens concluído.")
