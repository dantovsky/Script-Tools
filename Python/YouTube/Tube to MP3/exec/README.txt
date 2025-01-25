Para o funcionamento deste programa é necessário fazer downloado do FFMPEG e colocar no PC, por exemplo:
C:\Bins

Deopis precisa adicionar o caminho C:\Bins\ffmpeg\bin ao PATH das variáveis de sistema.

---

Para instalar o FFmpeg no Windows 11, siga estes passos:

01. Download:

	Acesse o site oficial do FFmpeg: FFmpeg Download (https://ffmpeg.org/download.html).
	Clique em "Windows" e depois selecione um site de distribuição, como "gyan.dev".

02. Escolha do Pacote:
	
	Na página do distribuidor, escolha o pacote "ffmpeg-release-essentials.zip".

03. Extração:

	Após o download, extraia o arquivo ZIP para uma pasta no seu computador, como C:\ffmpeg.

04. Configuração do PATH:

	Pressione Win + X e selecione "Sistema".
	Clique em "Configurações avançadas do sistema" e depois no botão "Variáveis de Ambiente".
	Encontre a variável "Path" na seção "Variáveis do sistema" e clique em "Editar".
	Adicione uma nova entrada com o caminho para a pasta bin do FFmpeg, por exemplo, C:\ffmpeg\bin.

05. Verificação:

	Abra o Prompt de Comando (Win + R, digite cmd e pressione Enter).
	Digite ffmpeg -version e pressione Enter. Se o FFmpeg estiver instalado corretamente, ele mostrará a versão instalada.
	Seguindo esses passos, o FFmpeg estará instalado e pronto para uso no seu sistema Windows 11.