// Espera o carregamento completo do HTML antes de executar o script
document.addEventListener("DOMContentLoaded", function () {

    // Pega o campo de busca
    const input = document.getElementById("search-input");

    // Pega a tabela de clientes
    const tabela = document.getElementById("tabela-clientes");

    // Se não encontrar input ou tabela, interrompe o código (evita erro)
    if (!input || !tabela) return;

    // Pega todas as linhas da tabela (tr)
    // slice(1) remove o cabeçalho
    const linhas = Array.from(tabela.getElementsByTagName("tr")).slice(1);

    // Tenta pegar a caixa de sugestões já existente
    let sugestoesBox = document.getElementById("sugestoes-box");

    // Se não existir, cria dinamicamente
    if (!sugestoesBox) {

        // Cria uma div
        sugestoesBox = document.createElement("div");

        // Define o id da div
        sugestoesBox.id = "sugestoes-box";

        // Adiciona classe CSS
        sugestoesBox.classList.add("lista-sugestoes");

        // Adiciona no body da página
        document.body.appendChild(sugestoesBox);
    }

    // Define estilos diretamente via JavaScript (CSS inline)
    sugestoesBox.style.position = "absolute";     // Permite posicionamento livre
    sugestoesBox.style.background = "white";      // Fundo branco
    sugestoesBox.style.border = "1px solid #ccc"; // Borda leve
    sugestoesBox.style.maxHeight = "150px";       // Altura máxima
    sugestoesBox.style.overflowY = "auto";        // Scroll vertical se necessário
    sugestoesBox.style.display = "none";          // Inicialmente escondido
    sugestoesBox.style.zIndex = "1000";           // Fica acima de outros elementos

    // Evento disparado ao digitar no input
    input.addEventListener("input", function () {

        // Pega o termo digitado em minúsculo
        const termo = input.value.toLowerCase();

        // Limpa sugestões anteriores
        sugestoesBox.innerHTML = "";

        // Se estiver vazio, esconde a caixa
        if (!termo) {
            sugestoesBox.style.display = "none";
            return;
        }

        // Gera os resultados
        const resultados = linhas

            // Pega o texto da segunda coluna (nome)
            .map(linha => linha.getElementsByTagName("td")[1].textContent)

            // Filtra pelo termo digitado
            .filter(nome => nome.toLowerCase().includes(termo));

        // Para cada resultado encontrado
        resultados.forEach(nome => {

            // Cria uma div para sugestão
            const div = document.createElement("div");

            // Define o texto da sugestão
            div.textContent = nome;

            // Adiciona classe CSS
            div.classList.add("item-sugestao");

            // Evento ao clicar na sugestão
            div.onclick = function () {

                // Preenche o input com o nome escolhido
                input.value = nome;

                // Limpa sugestões
                sugestoesBox.innerHTML = "";

                // Esconde a caixa
                sugestoesBox.style.display = "none";

                // Encontra a linha correspondente na tabela
                const linha = linhas.find(
                    l => l.getElementsByTagName("td")[1].textContent === nome
                );

                // Se encontrou a linha
                if (linha) {

                    // Faz scroll suave até ela
                    linha.scrollIntoView({ behavior: "smooth", block: "center" });

                    // Adiciona transição suave na cor
                    linha.style.transition = "background 0.5s";

                    // Destaca a linha
                    linha.style.backgroundColor = "#ffff99";

                    // Remove o destaque depois de 1.5 segundos
                    setTimeout(() => linha.style.backgroundColor = "", 1500);
                }
            };

            // Adiciona a sugestão na caixa
            sugestoesBox.appendChild(div);
        });

        // Se houver resultados, posiciona e mostra a caixa
        if (resultados.length > 0) {

            // Pega posição e tamanho do input na tela
            const rect = input.getBoundingClientRect();

            // Posiciona a caixa logo abaixo do input (considerando scroll)
            sugestoesBox.style.top = rect.bottom + window.scrollY + "px";

            // Alinha à esquerda do input
            sugestoesBox.style.left = rect.left + window.scrollX + "px";

            // Define mesma largura do input
            sugestoesBox.style.width = rect.width + "px";

            // Mostra a caixa
            sugestoesBox.style.display = "block";

        } else {

            // Se não tiver resultados, esconde
            sugestoesBox.style.display = "none";
        }
    });

    // Evento global para clique fora
    document.addEventListener("click", function (e) {

        // Se clicou fora do input e da caixa
        if (e.target !== input && !sugestoesBox.contains(e.target)) {

            // Esconde sugestões
            sugestoesBox.style.display = "none";
        }
    });

    // Evento de scroll da página
    window.addEventListener("scroll", function () {

        // Se a caixa estiver visível
        if (sugestoesBox.style.display === "block") {

            // Recalcula posição do input
            const rect = input.getBoundingClientRect();

            // Atualiza posição da caixa (mantém alinhada ao input)
            sugestoesBox.style.top = rect.bottom + window.scrollY + "px";
            sugestoesBox.style.left = rect.left + window.scrollX + "px";
        }
    });
});