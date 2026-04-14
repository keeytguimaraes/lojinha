// Espera o carregamento completo do HTML antes de executar o script
// Garante que todos os elementos da página já existam
document.addEventListener("DOMContentLoaded", function () {

    // =========================
    // ELEMENTOS PRINCIPAIS
    // =========================

    // Pega o campo de busca onde o usuário digita
    const input = document.getElementById("search-input");

    // Pega a tabela onde estão os dados dos ADMs
    const tabela = document.getElementById("tabela-adms");

    // Se não encontrar o input ou a tabela, interrompe o código
    // Isso evita erros ao tentar acessar elementos inexistentes
    if (!input || !tabela) return;

    // =========================
    // CAPTURA DAS LINHAS
    // =========================

    // Pega todas as linhas da tabela (<tr>)
    // Array.from → transforma em array real (permite usar map, filter, etc)
    // slice(1) → remove a primeira linha (cabeçalho)
    const linhas = Array.from(tabela.getElementsByTagName("tr")).slice(1);

    // =========================
    // CAIXA DE SUGESTÕES
    // =========================

    // Pega a div onde serão exibidas as sugestões (já existente no HTML)
    let sugestoesBox = document.getElementById("sugestoes-box");

    // =========================
    // EVENTO DE DIGITAÇÃO
    // =========================

    // Evento disparado sempre que o usuário digita algo no input
    input.addEventListener("input", function () {

        // Pega o texto digitado e converte para minúsculo
        // Isso evita problemas com comparação (maiúsculas/minúsculas)
        const termo = input.value.toLowerCase();

        // Limpa sugestões anteriores
        sugestoesBox.innerHTML = "";

        // Se o campo estiver vazio
        if (!termo) {

            // Esconde a caixa de sugestões
            sugestoesBox.style.display = "none";
            return;
        }

        // =========================
        // FILTRO DOS DADOS
        // =========================

        const resultados = linhas

            // Para cada linha, pega o conteúdo da segunda coluna (nome do ADM)
            .map(linha => linha.getElementsByTagName("td")[1].textContent)

            // Filtra apenas os nomes que contêm o termo digitado
            .filter(nome => nome.toLowerCase().includes(termo));

        // =========================
        // CRIAÇÃO DAS SUGESTÕES
        // =========================

        resultados.forEach(nome => {

            // Cria uma div para representar a sugestão
            const div = document.createElement("div");

            // Define o texto exibido na sugestão
            div.textContent = nome;

            // Adiciona classe CSS (usada para estilização visual)
            div.classList.add("item-sugestao");

            // =========================
            // EVENTO DE CLIQUE NA SUGESTÃO
            // =========================

            div.onclick = function () {

                // Preenche o input com o nome selecionado
                input.value = nome;

                // Limpa sugestões
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

                    // Destaca a linha com cor amarela
                    linha.style.backgroundColor = "#ffff99";

                    // Remove o destaque após 1.5 segundos
                    setTimeout(() => linha.style.backgroundColor = "", 1500);
                }
            };

            // Adiciona a sugestão dentro da caixa
            sugestoesBox.appendChild(div);
        });

        // =========================
        // CONTROLE DE VISIBILIDADE
        // =========================

        // Mostra a caixa se houver resultados, senão esconde
        sugestoesBox.style.display = resultados.length > 0 ? "block" : "none";
    });
});