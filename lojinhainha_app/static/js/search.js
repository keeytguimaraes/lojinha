document.addEventListener("DOMContentLoaded", function () {
    // Espera o HTML carregar completamente antes de executar o código
    // Isso garante que todos os elementos (input, tabela, etc.) já existam no DOM

    const input = document.getElementById("search-input");
    // Seleciona o campo de busca onde o usuário digita o nome

    const tabela = document.getElementById("tabela-vendedores");
    // Seleciona a tabela que contém os vendedores

    if (!input || !tabela) return;
    // Se não encontrar o input OU a tabela, interrompe o script
    // Evita erros como "cannot read property of null"

    const linhas = Array.from(tabela.getElementsByTagName("tr")).slice(1); 
    // Pega todas as linhas da tabela (tr)
    // Array.from → converte HTMLCollection em array manipulável
    // slice(1) → remove a primeira linha (cabeçalho da tabela)

    // =========================
    // CRIAÇÃO DA CAIXA DE SUGESTÕES
    // =========================
    let sugestoesBox = document.getElementById("sugestoes-box");
    // Tenta pegar a caixa de sugestões caso já exista no HTML

    if (!sugestoesBox) {
        sugestoesBox = document.createElement("div");
        // Cria a caixa de sugestões dinamicamente se não existir

        sugestoesBox.id = "sugestoes-box";
        // Define um ID para poder reutilizar depois

        sugestoesBox.classList.add("lista-sugestoes");
        // Adiciona classe CSS para estilização (cores, hover, etc)

        document.body.appendChild(sugestoesBox);
        // Adiciona a caixa diretamente no body da página
    }

    // =========================
    // ESTILIZAÇÃO DINÂMICA DA CAIXA
    // =========================
    sugestoesBox.style.position = "absolute";
    // Permite posicionar a caixa livremente na tela (em relação ao viewport)

    sugestoesBox.style.background = "white";
    // Define fundo branco

    sugestoesBox.style.border = "1px solid #ccc";
    // Adiciona uma borda cinza clara

    sugestoesBox.style.maxHeight = "150px";
    // Limita altura máxima da caixa

    sugestoesBox.style.overflowY = "auto";
    // Adiciona scroll vertical se ultrapassar a altura

    sugestoesBox.style.display = "none";
    // Começa escondida

    sugestoesBox.style.zIndex = "1000";
    // Garante que fique acima de outros elementos na tela

    // =========================
    // EVENTO DE DIGITAÇÃO
    // =========================
    input.addEventListener("input", function () {

        const termo = input.value.toLowerCase();
        // Pega o texto digitado e converte para minúsculo
        // Facilita comparação sem diferenciar maiúsculas/minúsculas

        sugestoesBox.innerHTML = "";
        // Limpa sugestões anteriores

        if (!termo) {
            sugestoesBox.style.display = "none";
            // Se o campo estiver vazio, esconde a caixa
            return;
        }

        // =========================
        // FILTRO DOS DADOS DA TABELA
        // =========================
        const resultados = linhas
            .map(linha => linha.getElementsByTagName("td")[1].textContent)
            // Para cada linha, pega o conteúdo da segunda coluna (nome do vendedor)

            .filter(nome => nome.toLowerCase().includes(termo));
            // Filtra apenas nomes que contêm o termo digitado

        // =========================
        // CRIAÇÃO DAS SUGESTÕES
        // =========================
        resultados.forEach(nome => {

            const div = document.createElement("div");
            // Cria uma nova div para cada sugestão

            div.textContent = nome;
            // Define o texto da sugestão

            div.classList.add("item-sugestao");
            // Adiciona classe CSS para estilo (hover, clique, etc)

            div.addEventListener("click", function () {
                // Evento ao clicar em uma sugestão

                input.value = nome;
                // Preenche o input com o nome selecionado

                sugestoesBox.innerHTML = "";
                // Limpa as sugestões

                sugestoesBox.style.display = "none";
                // Esconde a caixa de sugestões

                // =========================
                // SCROLL ATÉ A LINHA NA TABELA
                // =========================
                const linha = linhas.find(
                    l => l.getElementsByTagName("td")[1].textContent === nome
                );
                // Procura a linha da tabela correspondente ao nome clicado

                if (linha) {
                    linha.scrollIntoView({ behavior: "smooth", block: "center" });
                    // Faz a página rolar suavemente até a linha

                    linha.style.transition = "background 0.5s";
                    // Adiciona transição suave na mudança de cor

                    linha.style.backgroundColor = "#ffff99";
                    // Destaca a linha com cor amarela

                    setTimeout(() => linha.style.backgroundColor = "", 1500);
                    // Remove o destaque após 1.5 segundos
                }
            });

            sugestoesBox.appendChild(div);
            // Adiciona a sugestão na caixa
        });

        // =========================
        // POSICIONAMENTO DA CAIXA
        // =========================
        if (resultados.length > 0) {
            const rect = input.getBoundingClientRect();
            // Obtém posição e tamanho do input na tela

            sugestoesBox.style.top = rect.bottom + window.scrollY + "px";
            // Define posição vertical logo abaixo do input

            sugestoesBox.style.left = rect.left + window.scrollX + "px";
            // Define posição horizontal alinhada com o input

            sugestoesBox.style.width = rect.width + "px";
            // Define a largura igual à do input

            sugestoesBox.style.display = "block";
            // Exibe a caixa de sugestões
        } else {
            sugestoesBox.style.display = "none";
            // Se não houver resultados, esconde a caixa
        }
    });

    // =========================
    // FECHAR AO CLICAR FORA
    // =========================
    document.addEventListener("click", function (e) {
        if (e.target !== input && !sugestoesBox.contains(e.target)) {
            // Se o clique não foi no input nem dentro da caixa

            sugestoesBox.style.display = "none";
            // Esconde a caixa de sugestões
        }
    });

    // =========================
    // AJUSTE AO ROLAR A PÁGINA
    // =========================
    window.addEventListener("scroll", function () {
        if (sugestoesBox.style.display === "block") {
            // Se a caixa estiver visível

            const rect = input.getBoundingClientRect();
            // Recalcula a posição do input

            sugestoesBox.style.top = rect.bottom + window.scrollY + "px";
            sugestoesBox.style.left = rect.left + window.scrollX + "px";
            // Atualiza posição da caixa para acompanhar o scroll
        }
    });
});