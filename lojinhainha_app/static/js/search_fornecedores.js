// Espera o carregamento completo do HTML antes de executar o script
document.addEventListener("DOMContentLoaded", function () {

    // Pega o campo de busca
    const input = document.getElementById("search-input");

    // Pega a tabela de fornecedores
    const tabela = document.getElementById("tabela-fornecedores");

    // Se não existir input ou tabela, interrompe execução (evita erro)
    if (!input || !tabela) return;

    // Pega todas as linhas da tabela, ignorando o cabeçalho
    const linhas = Array.from(tabela.getElementsByTagName("tr")).slice(1);

    // Tenta pegar a caixa de sugestões já existente
    let sugestoesBox = document.getElementById("sugestoes-box");

    // Se não existir, cria dinamicamente
    if (!sugestoesBox) {

        // Cria uma div
        sugestoesBox = document.createElement("div");

        // Define o id
        sugestoesBox.id = "sugestoes-box";

        // Adiciona classe CSS
        sugestoesBox.classList.add("lista-sugestoes");

        // Adiciona ao body da página
        document.body.appendChild(sugestoesBox);
    }

    //  DEFINE ESTILOS INLINE (mesmo padrão dos outros módulos)
    sugestoesBox.style.position = "absolute";     // Permite posicionamento livre
    sugestoesBox.style.background = "white";      // Fundo branco
    sugestoesBox.style.border = "1px solid #ccc"; // Borda leve
    sugestoesBox.style.maxHeight = "150px";       // Altura máxima
    sugestoesBox.style.overflowY = "auto";        // Scroll vertical
    sugestoesBox.style.display = "none";          // Começa escondido
    sugestoesBox.style.zIndex = "1000";           // Fica acima de outros elementos

    // Evento ao digitar no input
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

        // Gera lista de resultados
        const resultados = linhas

            // Pega o conteúdo da segunda coluna (índice 1)
            .map(linha => linha.getElementsByTagName("td")[1].textContent)

            // Filtra nomes que contenham o termo digitado
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

                // Preenche o input com o valor escolhido
                input.value = nome;

                // Limpa sugestões
                sugestoesBox.innerHTML = "";

                // Esconde a caixa
                sugestoesBox.style.display = "none";

                // Procura a linha correspondente na tabela
                const linha = linhas.find(l =>
                    l.getElementsByTagName("td")[1].textContent === nome
                );

                // Se encontrar a linha
                if (linha) {

                    // Scroll suave até a linha
                    linha.scrollIntoView({ behavior: "smooth", block: "center" });

                    // Adiciona transição suave
                    linha.style.transition = "background 0.5s";

                    // Destaca a linha
                    linha.style.backgroundColor = "#ffff99";

                    // Remove destaque após 1.5 segundos
                    setTimeout(() => linha.style.backgroundColor = "", 1500);
                }
            };

            // Adiciona sugestão na caixa
            sugestoesBox.appendChild(div);
        });

        //  POSICIONAMENTO DINÂMICO
        if (resultados.length > 0) {

            // Pega posição do input
            const rect = input.getBoundingClientRect();

            // Posiciona abaixo do input considerando scroll
            sugestoesBox.style.top = rect.bottom + window.scrollY + "px";

            // Alinha à esquerda
            sugestoesBox.style.left = rect.left + window.scrollX + "px";

            // Define largura igual ao input
            sugestoesBox.style.width = rect.width + "px";

            // Mostra a caixa
            sugestoesBox.style.display = "block";

        } else {

            // Esconde se não houver resultados
            sugestoesBox.style.display = "none";
        }
    });

    // Fecha sugestões ao clicar fora
    document.addEventListener("click", function (e) {

        // Se o clique não foi no input nem na caixa
        if (e.target !== input && !sugestoesBox.contains(e.target)) {

            // Esconde sugestões
            sugestoesBox.style.display = "none";
        }
    });

    // Ajusta posição ao rolar a página
    window.addEventListener("scroll", function () {

        // Se a caixa estiver visível
        if (sugestoesBox.style.display === "block") {

            // Recalcula posição do input
            const rect = input.getBoundingClientRect();

            // Atualiza posição da caixa
            sugestoesBox.style.top = rect.bottom + window.scrollY + "px";
            sugestoesBox.style.left = rect.left + window.scrollX + "px";
        }
    });
});