# Bulk Images Tools

Este Github "Bulk Images Tools" possui as seguintes ferramentas:

01. Download Images From URL List and Compress: faz download de imagens a partir de URLs e comprime.
02. Modify Image Names and Compress: altera imagens a partir de uma pasta no computador.

## Pré-requisitos

Deverá instalar no computador o Python versão 3.x

Instalar as dependências:
`pip install pillow`

Veja as instruções específicas de utilização para cada programa.

## 01. Download Images From URL List and Compress

Faz download de imagens a partir de URLs e comprime.

Primeiro você pode configurar os seguintes parâmetros:
- Qual será a pasta de destino no computador
- Nome base das imagens (depois elas serão diferenciadas com a inclusão de um número ao final)
- Tamanho máximo para as imagens horizontais
- Tamanho máximo para as imagens quadradas
- Tamanho máximo para as imagens verticais
- Qualidade de compressão
- Opção se quer que seja comprimida e resized ('False' apenas comprime)

É necessário colocar o URL de cada imagem como um item da lista `url_image_list`. Exemplo de estrutura para fazer o download de 3 imagens a partir de suas URLs:
```py
url_image_list = [
    { "url": "https://nomedosite.com/nomedaimagem_1.jpg" },
    { "url": "https://nomedosite.com/nomedaimagem_2.jpg" },
    { "url": "https://nomedosite.com/nomedaimagem_3.jpg" },
]
```

Na linha de comandos correr o comando:
`python download-img-and-compress.py`

O resultado irá para a pasta de destino.

## 02. Modify Image Names and Compress

Altera imagens a partir de uma pasta no computador.

Primeiro você pode configurar os seguintes parâmetros:
- Qual será a pasta de origem no computador
- Qual será a pasta de destino no computador
- Nome base das imagens (depois elas serão diferenciadas com a inclusão de um número ao final)
- Tamanho máximo para as imagens horizontais
- Tamanho máximo para as imagens quadradas
- Tamanho máximo para as imagens verticais
- Qualidade de compressão

Então deverá colocar as imagens na pasta de origem.

Na linha de comandos correr o comando:
`python modify-image-names-and-compress.py`

O resultado irá para a pasta de destino.`

## Help Links

pillow 10.2.0  
https://pypi.org/project/pillow/

## TODO

Analisar sobre a compressão de imagens GIF, podendo ser de ajuda o seguinte link:  
Pillow - Resizing a GIF 
https://stackoverflow.com/questions/41718892/pillow-resizing-a-gif
