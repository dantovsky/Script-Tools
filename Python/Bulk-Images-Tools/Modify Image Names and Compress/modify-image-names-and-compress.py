from PIL import Image, ExifTags
import os

# Program Name: Modify Image Names and Compress
# About: Change image names, compress and resize (quality and dimension) from a folder in computer and output to other folder
# Author: Dante Marinho and ChatGPT (Portugal)
# Date: 19/12/2023

# Configuradores
source_folder = ".\images_from" # Pasta de origem das imagens
destination_folder = ".\images_out" # Pasta de destino
base_name = "nome da minha foto"
max_horizontal_width = 1400
max_square_width = 1200
max_vertical_width = 700
compression_quality = 72 # Ajuste conforme necessário
initial_photo_number = False # Deixar o valro = False se quiser que começe a partir do número 1

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

        print(f"Imagem processada: {output_path}")

    except Exception as e:
        print(f"Erro ao processar a imagem {image_path}: {e}")

# Lista de arquivos na pasta de origem
image_files = [f for f in os.listdir(source_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))] # Nao suporta GIF muito bem ainda

# Loop através dos arquivos de imagem na pasta de origem
for i, image_file in enumerate(image_files):
    # Cria o caminho completo para a imagem de origem
    image_path = os.path.join(source_folder, image_file)

    # Obtem a extensao do ficheiro
    image_extension = image_file.split(".")[-1]  

    # Modifica o nome do arquivo
    new_file_name = f"{base_name} {initial_photo_number + i}.{image_extension}" if initial_photo_number != False else f"{base_name} {i + 1}.{image_extension}"
    new_file_path = os.path.join(destination_folder, new_file_name)

    # Comprime e redimensiona a imagem
    compress_and_resize_image(image_path, new_file_path)

print("Processamento de imagens concluído.")
