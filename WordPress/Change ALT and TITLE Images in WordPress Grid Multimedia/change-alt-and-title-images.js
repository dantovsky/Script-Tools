/**
 * ~ ~ ~ Change ALT and TITLE Images in WordPress Grid Multimedia ~ ~ ~
 * 
 * Author: Dante Marinho e ChatGPT v4
 * 
 * Instruções de uso:
 * A paritr de uma imagem do WordPress, em "grid mode", esse script altera uma sequência de imagens a partir desta 1ª imagem.
 * O script altera os campos ALT TEXT e o TITLE e em seguida clica no botão de passar para a próxima imagem à direita.
 * 
 * Parâmetros:
 * - texto a ser adicionado
 * - limite de imagens para ser alterada
 */

(function alterarTextosEmImagens(texto, limite) {
    let contador = 0;

    function atualizarTextoEProximaImagem() {
        if (contador >= limite) {
            console.log('Concluído. Número de imagens atualizadas:', contador);
            return;
        }

        // Encontrar e atualizar os campos de texto ALT e Título
        const campoAltText = document.getElementById("attachment-details-two-column-alt-text");
        const campoTitulo = document.getElementById("attachment-details-two-column-title");
        if (campoAltText && campoTitulo) {
            campoAltText.value = texto; // Atualiza o ALT Text
            campoTitulo.value = texto; // Atualiza o Título
            contador++;
            console.log('Imagem atualizada:', contador);
        }

        // Clica no botão para editar a próxima imagem
        const botaoProximaImagem = document.querySelector('button.right.dashicons');
        if (botaoProximaImagem) {
            botaoProximaImagem.click();
        }

        // Aguarda um pouco antes de processar a próxima imagem, para garantir que a página tenha sido atualizada
        setTimeout(atualizarTextoEProximaImagem, 200);
    }

    atualizarTextoEProximaImagem();
})("Missão Humanitária Guiné Bissau 2017", 92); // Exemplo de uso: altera o ALT Text e Título de 5 imagens para "Texto para inserir"
