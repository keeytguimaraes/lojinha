// Espera o carregamento completo do HTML antes de executar o script
// Isso garante que todos os elementos já existam no DOM
document.addEventListener("DOMContentLoaded", function () {

    // =========================
    // ELEMENTOS PRINCIPAIS
    // =========================

    // Pega o campo de busca onde o usuário digita
    const input = document.getElementById("search-input");

    // Pega a tabela de clientes exibida na tela
    const tabela = document.getElementById("tabela-clientes");

    // Se não encontrar o input ou a tabela, interrompe o código
    // Isso evita erros de execução (ex: acessar propriedades de null)
    if (!input || !tabela) return;

    // =========================
    // CAPTURA DAS LINHAS
    // =========================

    // Pega todas as linhas da tabela (elementos <tr>)
    // Array.from → transforma em array real (para usar map, filter, etc)
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

        // Define o ID da div (para reutilização futura)
        sugestoesBox.id = "sugestoes-box";

        // Adiciona uma classe CSS para estilização
        sugestoesBox.classList.add("lista-sugestoes");

        // Adiciona a div no body da página
        document.body.appendChild(sugestoesBox);
    }

    // =========================
    // ESTILIZAÇÃO DA CAIXA
    // =========================

    sugestoesBox.style.position = "absolute";     
    // Permite posicionamento livre na tela

    sugestoesBox.style.background = "white";      
    // Define fundo branco

    sugestoesBox.style.border = "1px solid #ccc"; 
    // Define borda leve cinza

    sugestoesBox.style.maxHeight = "150px";       
    // Limita a altura máxima da caixa

    sugestoesBox.style.overflowY = "auto";        
    // Adiciona scroll vertical se necessário

    sugestoesBox.style.display = "none";          
    // Inicialmente escondido

    sugestoesBox.style.zIndex = "1000";           
    // Garante que fique acima de outros elementos

    // =========================
    // EVENTO DE DIGITAÇÃO
    // =========================

    input.addEventListener("input", function () {

        // Pega o texto digitado e transforma em minúsculo
        // Isso evita problemas com maiúsculas/minúsculas
        const termo = input.value.toLowerCase();

        // Limpa todas as sugestões anteriores
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

            // Para cada linha da tabela, pega o conteúdo da segunda coluna (nome do cliente)
            .map(linha => linha.getElementsByTagName("td")[1].textContent)

            // Filtra apenas os nomes que contêm o termo digitado
            .filter(nome => nome.toLowerCase().includes(termo));

        // =========================
        // CRIAÇÃO DAS SUGESTÕES
        // =========================

        resultados.forEach(nome => {

            // Cria uma div para cada sugestão
            const div = document.createElement("div");

            // Define o texto que será exibido
            div.textContent = nome;

            // Adiciona classe CSS (usada para estilo visual)
            div.classList.add("item-sugestao");

            // =========================
            // EVENTO DE CLIQUE NA SUGESTÃO
            // =========================

            div.onclick = function () {

                // Preenche o input com o nome selecionado
                input.value = nome;

                // Limpa as sugestões
                sugestoesBox.innerHTML = "";

                // Esconde a caixa de sugestões
                sugestoesBox.style.display = "none";

                // =========================
                // BUSCA DA LINHA NA TABELA
                // =========================

                const linha = linhas.find(
                    l => l.getElementsByTagName("td")[1].textContent === nome
                );

                // =========================
                // SCROLL + DESTAQUE
                // =========================

                if (linha) {

                    // Faz scroll suave até a linha encontrada
                    linha.scrollIntoView({ behavior: "smooth", block: "center" });

                    // Aplica transição suave na mudança de cor
                    linha.style.transition = "background 0.5s";

                    // Destaca a linha com cor amarela
                    linha.style.backgroundColor = "#ffff99";

                    // Remove o destaque após 1.5 segundos
                    setTimeout(() => linha.style.backgroundColor = "", 1500);
                }
            };

            // Adiciona a sugestão na caixa
            sugestoesBox.appendChild(div);
        });

        // =========================
        // POSICIONAMENTO DINÂMICO
        // =========================

        // Se houver resultados, mostra a caixa
        if (resultados.length > 0) {

            // Pega posição e tamanho do input
            const rect = input.getBoundingClientRect();

            // Posiciona a caixa abaixo do input (considerando scroll da página)
            sugestoesBox.style.top = rect.bottom + window.scrollY + "px";

            // Alinha horizontalmente com o input
            sugestoesBox.style.left = rect.left + window.scrollX + "px";

            // Define a mesma largura do input
            sugestoesBox.style.width = rect.width + "px";

            // Exibe a caixa
            sugestoesBox.style.display = "block";

        } else {

            // Se não houver resultados, esconde
            sugestoesBox.style.display = "none";
        }
    });

    // =========================
    // FECHAR AO CLICAR FORA
    // =========================

    document.addEventListener("click", function (e) {

        // Se o clique não foi no input nem na caixa
        if (e.target !== input && !sugestoesBox.contains(e.target)) {

            // Esconde a caixa de sugestões
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