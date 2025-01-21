// ==UserScript==
// @name         YouTube Title Copy Button
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Adiciona um botão para copiar o título e URL de vídeos do YouTube
// @author       Você
// @match        https://www.youtube.com/*
// @grant        GM_setClipboard
// ==/UserScript==

(function() {
    'use strict';

    // Função para criar o botão
    function addCopyButton() {
        // Verificar se já existe o botão para evitar múltiplas inserções
        if (document.querySelector('#copy-title-button')) return;

        // Obter o elemento do título (h1)
        // onst titleElement = document.querySelector('h1.title.ytd-video-primary-info-renderer');
        const titleDiv = document.querySelector('#above-the-fold div#title');
        const titleElement = document.querySelector('#title h1');

        if (!titleDiv || !titleElement) {
            console.log('O título ainda não foi renderizado');
            return;
        }

        // CSS para o título
        titleDiv.style.display = 'inline-flex';
        titleDiv.style.alignItems = 'center';

        // Criar o botão
        const copyButton = document.createElement('button');
        copyButton.id = 'copy-title-button';
        copyButton.textContent = 'Copy';
        copyButton.style.marginLeft = '8px';
        copyButton.style.padding = '5px 10px';
        copyButton.style.fontSize = '14px';
        copyButton.style.cursor = 'pointer';
        copyButton.style.backgroundColor = '#139dff';
        copyButton.style.color = 'white';
        copyButton.style.border = 'none';
        copyButton.style.borderRadius = '5px';

        // Adicionar evento de clique
        copyButton.addEventListener('click', () => {
            const videoTitle = titleElement.textContent.trim();
            const videoURL = window.location.href;
            const output = `${videoTitle}\n${videoURL}`;

            // Copiar para o clipboard
            GM_setClipboard(output);
            console.log('Copiado para o clipboard:\n' + output);

            // Efeito visual
            const divConfirmation = document.createElement('span');
            divConfirmation.style.fontSize = '14px';
            divConfirmation.style.marginLeft = '8px';
            divConfirmation.textContent = 'Título e URL copiados!'
            copyButton.after(divConfirmation);
            copyButton.style.backgroundColor = '#58cf39';
            setTimeout(() => {
                copyButton.style.backgroundColor = '#139dff';
                divConfirmation.style.display = 'none';
            }, 3000)
        });

        // Adicionar o botão ao lado do título
        titleElement.after(copyButton);
    }

    // Observar mudanças na página para adicionar o botão dinamicamente
    const observer = new MutationObserver(() => {
        addCopyButton();
    });

    observer.observe(document.body, { childList: true, subtree: true });
})();
