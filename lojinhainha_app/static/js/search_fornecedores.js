// Espera o carregamento completo do HTML antes de executar o script
// Garante que todos os elementos já estejam disponíveis no DOM
document.addEventListener("DOMContentLoaded", function () {

    // =========================
    // ELEMENTOS PRINCIPAIS
    // =========================

    // Pega o campo de busca (input onde o usuário digita)
    const input = document.getElementById("search-input");

    // Pega a tabela de fornecedores
    const tabela = document.getElementById("tabela-fornecedores");

    // Se não existir input ou tabela, interrompe execução
    // Evita erros de referência (null)
    if (!input || !tabela) return;

    // =========================
    // CAPTURA DAS LINHAS
    // =========================

    // Pega todas as linhas da tabela (tr)
    // Array.from → converte HTMLCollection em array manipulável
    // slice(1) → remove o cabeçalho da tabela
    const linhas = Array.from(tabela.getElementsByTagName("tr")).slice(1);

    // =========================
    // CAIXA DE SUGESTÕES
    // =========================

    // Tenta pegar a caixa de sugestões já existente no HTML
    let sugestoesBox = document.getElementById("sugestoes-box");

    // Se não existir, cria dinamicamente
    if (!sugestoesBox) {

        // Cria uma nova div
        sugestoesBox = document.createElement("div");

        // Define um ID para reutilização futura
        sugestoesBox.id = "sugestoes-box";

        // Adiciona classe CSS para estilização
        sugestoesBox.classList.add("lista-sugestoes");

        // Adiciona a caixa no body da página
        document.body.appendChild(sugestoesBox);
    }

    // =========================
    // ESTILIZAÇÃO PADRÃO
    // =========================
    sugestoesBox.style.position = "absolute";     
    // Permite posicionamento livre na tela

    sugestoesBox.style.background = "white";      
    // Fundo branco

    sugestoesBox.style.border = "1px solid #ccc"; 
    // Borda leve cinza

    sugestoesBox.style.maxHeight = "150px";       
    // Altura máxima da caixa

    sugestoesBox.style.overflowY = "auto";        
    // Scroll vertical se necessário

    sugestoesBox.style.display = "none";          
    // Começa escondida

    sugestoesBox.style.zIndex = "1000";           
    // Fica acima de outros elementos

    // =========================
    // EVENTO DE DIGITAÇÃO
    // =========================
    input.addEventListener("input", function () {

        // Pega o termo digitado e transforma em minúsculo
        const termo = input.value.toLowerCase();

        // Limpa sugestões anteriores
        sugestoesBox.innerHTML = "";

        // Se estiver vazio, esconde a caixa
        if (!termo) {
            sugestoesBox.style.display = "none";
            return;
        }

        // =========================
        // FILTRO DOS DADOS
        // =========================
        const resultados = linhas

            // Para cada linha, pega o conteúdo da segunda coluna (nome do fornecedor)
            .map(linha => linha.getElementsByTagName("td")[1].textContent)

            // Filtra nomes que contenham o termo digitado
            .filter(nome => nome.toLowerCase().includes(termo));

        // =========================
        // CRIAÇÃO DAS SUGESTÕES
        // =========================
        resultados.forEach(nome => {

            // Cria uma div para cada sugestão
            const div = document.createElement("div");

            // Define o texto exibido
            div.textContent = nome;

            // Adiciona classe CSS para estilização (hover, etc)
            div.classList.add("item-sugestao");

            // =========================
            // EVENTO DE CLIQUE
            // =========================
            div.onclick = function () {

                // Preenche o input com o valor selecionado
                input.value = nome;

                // Limpa sugestões
                sugestoesBox.innerHTML = "";

                // Esconde a caixa
                sugestoesBox.style.display = "none";

                // =========================
                // BUSCA DA LINHA NA TABELA
                // =========================
                const linha = linhas.find(l =>
                    l.getElementsByTagName("td")[1].textContent === nome
                );

                // =========================
                // SCROLL + DESTAQUE
                // =========================
                if (linha) {

                    // Scroll suave até a linha correspondente
                    linha.scrollIntoView({ behavior: "smooth", block: "center" });

                    // Adiciona transição suave na mudança de cor
                    linha.style.transition = "background 0.5s";

                    // Destaca a linha
                    linha.style.backgroundColor = "#ffff99";

                    // Remove destaque após 1.5 segundos
                    setTimeout(() => linha.style.backgroundColor = "", 1500);
                }
            };

            // Adiciona a sugestão na caixa
            sugestoesBox.appendChild(div);
        });

        // =========================
        // POSICIONAMENTO DINÂMICO
        // =========================
        if (resultados.length > 0) {

            // Obtém posição e tamanho do input
            const rect = input.getBoundingClientRect();

            // Posiciona a caixa logo abaixo do input (considerando scroll)
            sugestoesBox.style.top = rect.bottom + window.scrollY + "px";

            // Alinha horizontalmente com o input
            sugestoesBox.style.left = rect.left + window.scrollX + "px";

            // Define mesma largura do input
            sugestoesBox.style.width = rect.width + "px";

            // Exibe a caixa
            sugestoesBox.style.display = "block";

        } else {

            // Esconde se não houver resultados
            sugestoesBox.style.display = "none";
        }
    });

    // =========================
    // FECHAR AO CLICAR FORA
    // =========================
    document.addEventListener("click", function (e) {

        // Se o clique não foi no input nem dentro da caixa
        if (e.target !== input && !sugestoesBox.contains(e.target)) {

            // Esconde sugestões
            sugestoesBox.style.display = "none";
        }
    });

    // =========================
    // AJUSTE AO ROLAR A PÁGINA
    // =========================
    window.addEventListener("scroll", function () {

        // Se a caixa estiver visível
        if (sugestoesBox.style.display === "block") {

            // Recalcula posição do input
            const rect = input.getBoundingClientRect();

            // Atualiza posição da caixa para acompanhar o scroll
            sugestoesBox.style.top = rect.bottom + window.scrollY + "px";
            sugestoesBox.style.left = rect.left + window.scrollX + "px";
        }
    });
});