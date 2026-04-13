document.addEventListener("DOMContentLoaded", function () {
    // Espera o HTML carregar completamente antes de executar o código

    const input = document.getElementById("search-input");
    // Pega o campo de busca onde o usuário digita

    const tabela = document.getElementById("tabela-vendedores");
    // Pega a tabela de vendedores

    if (!input || !tabela) return;
    // Se não encontrar o input ou a tabela, para a execução para evitar erro

    const linhas = Array.from(tabela.getElementsByTagName("tr")).slice(1); 
    // Pega todas as linhas da tabela (tr)
    // slice(1) remove o cabeçalho (primeira linha)

    // Cria ou pega o container de sugestões
    let sugestoesBox = document.getElementById("sugestoes-box");
    // Tenta pegar a caixa de sugestões já existente

    if (!sugestoesBox) {
        sugestoesBox = document.createElement("div");
        // Cria a caixa de sugestões caso não exista

        sugestoesBox.id = "sugestoes-box";
        // Define o ID da caixa

        sugestoesBox.classList.add("lista-sugestoes");
        // Adiciona uma classe CSS para estilização

        document.body.appendChild(sugestoesBox);
        // Adiciona a caixa no body da página
    }

    // Aplica estilo básico igual autocomplete cliente
    sugestoesBox.style.position = "absolute";
    // Permite posicionar a caixa em relação à tela

    sugestoesBox.style.background = "white";
    // Fundo branco

    sugestoesBox.style.border = "1px solid #ccc";
    // Borda cinza clara

    sugestoesBox.style.maxHeight = "150px";
    // Altura máxima da caixa

    sugestoesBox.style.overflowY = "auto";
    // Adiciona scroll vertical se passar do limite

    sugestoesBox.style.display = "none";
    // Começa escondida

    sugestoesBox.style.zIndex = "1000";
    // Garante que fique acima de outros elementos

    input.addEventListener("input", function () {
        // Evento disparado sempre que o usuário digita

        const termo = input.value.toLowerCase();
        // Pega o valor digitado e transforma em minúsculo

        sugestoesBox.innerHTML = "";
        // Limpa as sugestões anteriores

        if (!termo) {
            sugestoesBox.style.display = "none";
            // Se não tiver nada digitado, esconde a caixa
            return;
        }

        // Filtra nomes na tabela
        const resultados = linhas
            .map(linha => linha.getElementsByTagName("td")[1].textContent)
            // Pega o nome do vendedor (segunda coluna da tabela)

            .filter(nome => nome.toLowerCase().includes(termo));
            // Filtra apenas os nomes que contém o texto digitado

        resultados.forEach(nome => {
            // Para cada resultado encontrado

            const div = document.createElement("div");
            // Cria uma opção de sugestão

            div.textContent = nome;
            // Define o texto da sugestão

            div.classList.add("item-sugestao");
            // Adiciona classe para estilização

            div.addEventListener("click", function () {
                // Quando o usuário clica na sugestão

                input.value = nome;
                // Preenche o input com o nome selecionado

                sugestoesBox.innerHTML = "";
                // Limpa as sugestões

                sugestoesBox.style.display = "none";
                // Esconde a caixa

                // Rola até a linha correspondente
                const linha = linhas.find(l => l.getElementsByTagName("td")[1].textContent === nome);
                // Procura a linha da tabela com esse nome

                if (linha) {
                    linha.scrollIntoView({ behavior: "smooth", block: "center" });
                    // Faz a página rolar até a linha

                    linha.style.transition = "background 0.5s";
                    // Aplica transição suave

                    linha.style.backgroundColor = "#ffff99";
                    // Destaca a linha com cor amarela

                    setTimeout(() => linha.style.backgroundColor = "", 1500);
                    // Remove o destaque depois de 1.5 segundos
                }
            });

            sugestoesBox.appendChild(div);
            // Adiciona a sugestão na caixa
        });

        // Posiciona o container embaixo do input
        if (resultados.length > 0) {
            const rect = input.getBoundingClientRect();
            // Pega a posição do input na tela

            sugestoesBox.style.top = rect.bottom + window.scrollY + "px";
            // Define a posição vertical da caixa

            sugestoesBox.style.left = rect.left + window.scrollX + "px";
            // Define a posição horizontal da caixa

            sugestoesBox.style.width = rect.width + "px";
            // Faz a largura da caixa igual ao input

            sugestoesBox.style.display = "block";
            // Mostra a caixa
        } else {
            sugestoesBox.style.display = "none";
            // Se não tiver resultados, esconde
        }
    });

    // Fecha sugestões ao clicar fora
    document.addEventListener("click", function (e) {
        if (e.target !== input && !sugestoesBox.contains(e.target)) {
            // Se clicar fora do input e fora da caixa

            sugestoesBox.style.display = "none";
            // Esconde a caixa
        }
    });

    // Ajusta posição se rolar a página
    window.addEventListener("scroll", function () {
        if (sugestoesBox.style.display === "block") {
            // Se a caixa estiver visível

            const rect = input.getBoundingClientRect();
            // Recalcula posição do input

            sugestoesBox.style.top = rect.bottom + window.scrollY + "px";
            sugestoesBox.style.left = rect.left + window.scrollX + "px";
            // Atualiza posição da caixa para acompanhar o scroll
        }
    });
});