// Espera o HTML carregar completamente antes de executar o script
// Isso evita erros ao tentar acessar elementos que ainda não existem
document.addEventListener("DOMContentLoaded", function () {

    // =========================
    // ELEMENTOS PRINCIPAIS
    // =========================

    // Campo de busca onde o usuário digita
    const input = document.getElementById("search-input");

    // Tabela de estoque exibida na página
    const tabela = document.getElementById("tabela-estoque");

    // Se não encontrar o input OU a tabela, interrompe execução
    // Isso evita erros como "cannot read property of null"
    if (!input || !tabela) return;

    // =========================
    // CAPTURA DAS LINHAS
    // =========================

    // Pega todas as linhas da tabela (tr)
    // Array.from → transforma em array real
    // slice(1) → remove a primeira linha (cabeçalho)
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

        // Define um ID para poder reutilizar depois
        sugestoesBox.id = "sugestoes-box";

        // Adiciona classe CSS (para estilização)
        sugestoesBox.classList.add("lista-sugestoes");

        // Adiciona a div no body da página
        document.body.appendChild(sugestoesBox);
    }

    // =========================
    // ESTILIZAÇÃO DA CAIXA
    // =========================

    sugestoesBox.style.position = "absolute";     
    // Permite posicionar livremente na tela

    sugestoesBox.style.background = "white";      
    // Define fundo branco

    sugestoesBox.style.border = "1px solid #ccc"; 
    // Borda leve cinza

    sugestoesBox.style.maxHeight = "150px";       
    // Limita altura máxima

    sugestoesBox.style.overflowY = "auto";        
    // Adiciona scroll vertical se necessário

    sugestoesBox.style.display = "none";          
    // Começa escondida

    sugestoesBox.style.zIndex = "1000";           
    // Garante que fique acima de outros elementos

    // =========================
    // EVENTO DE DIGITAÇÃO
    // =========================

    input.addEventListener("input", function () {

        // Pega o valor digitado e transforma em minúsculo
        // Isso evita problemas com letras maiúsculas/minúsculas
        const termo = input.value.toLowerCase();

        // Limpa sugestões anteriores
        sugestoesBox.innerHTML = "";

        // Se o campo estiver vazio, esconde a caixa
        if (!termo) {
            sugestoesBox.style.display = "none";
            return;
        }

        // =========================
        // FILTRO DOS DADOS
        // =========================

        const resultados = linhas

            // Para cada linha, pega o conteúdo da segunda coluna (índice 1)
            .map(linha => linha.getElementsByTagName("td")[1].textContent)

            // Filtra apenas os nomes que contêm o termo digitado
            .filter(nome => nome.toLowerCase().includes(termo));

        // =========================
        // CRIAÇÃO DAS SUGESTÕES
        // =========================

        resultados.forEach(nome => {

            // Cria uma div para cada sugestão
            const div = document.createElement("div");

            // Define o texto que será exibido na sugestão
            div.textContent = nome;

            // Adiciona classe CSS (para hover, estilo, etc)
            div.classList.add("item-sugestao");

            // =========================
            // EVENTO DE CLIQUE NA SUGESTÃO
            // =========================

            div.onclick = function () {

                // Preenche o input com o valor selecionado
                input.value = nome;

                // Limpa sugestões
                sugestoesBox.innerHTML = "";

                // Esconde a caixa
                sugestoesBox.style.display = "none";

                // =========================
                // LOCALIZA A LINHA NA TABELA
                // =========================

                const linha = linhas.find(l =>
                    l.getElementsByTagName("td")[1].textContent === nome
                );

                // =========================
                // SCROLL + DESTAQUE
                // =========================

                if (linha) {

                    // Rola suavemente até a linha encontrada
                    linha.scrollIntoView({ behavior: "smooth", block: "center" });

                    // Adiciona efeito de transição na cor
                    linha.style.transition = "background 0.5s";

                    // Destaca a linha (amarelo)
                    linha.style.backgroundColor = "#ffff99";

                    // Remove o destaque após 1.5 segundos
                    setTimeout(() => linha.style.backgroundColor = "", 1500);
                }
            };

            // Adiciona a sugestão dentro da caixa
            sugestoesBox.appendChild(div);
        });

        // =========================
        // POSICIONAMENTO DINÂMICO
        // =========================

        if (resultados.length > 0) {

            // Obtém posição e tamanho do input
            const rect = input.getBoundingClientRect();

            // Posiciona a caixa logo abaixo do input (considerando scroll da página)
            sugestoesBox.style.top = rect.bottom + window.scrollY + "px";

            // Alinha horizontalmente com o input
            sugestoesBox.style.left = rect.left + window.scrollX + "px";

            // Define a mesma largura do input
            sugestoesBox.style.width = rect.width + "px";

            // Mostra a caixa
            sugestoesBox.style.display = "block";

        } else {

            // Se não houver resultados, esconde a caixa
            sugestoesBox.style.display = "none";
        }
    });

    // =========================
    // FECHAR AO CLICAR FORA
    // =========================

    document.addEventListener("click", function (e) {

        // Se o clique não foi no input nem na caixa de sugestões
        if (e.target !== input && !sugestoesBox.contains(e.target)) {

            // Esconde a caixa
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