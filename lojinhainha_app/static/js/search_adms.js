// Espera o carregamento completo do HTML antes de executar o script
document.addEventListener("DOMContentLoaded", function () {

    // Pega o campo de busca
    const input = document.getElementById("search-input");

    // Pega a tabela onde estão os dados (ADMs)
    const tabela = document.getElementById("tabela-adms");

    // Se não encontrar o input ou a tabela, o código para aqui (evita erro)
    if (!input || !tabela) return;

    // Pega todas as linhas da tabela (tr)
    // slice(1) remove a primeira linha (geralmente o cabeçalho)
    const linhas = Array.from(tabela.getElementsByTagName("tr")).slice(1);

    // Pega a div onde serão exibidas as sugestões
    let sugestoesBox = document.getElementById("sugestoes-box");

    // Evento disparado sempre que o usuário digita
    input.addEventListener("input", function () {

        // Pega o texto digitado e transforma em minúsculo
        const termo = input.value.toLowerCase();

        // Limpa sugestões anteriores
        sugestoesBox.innerHTML = "";

        // Se não tiver termo digitado
        if (!termo) {

            // Esconde a caixa de sugestões
            sugestoesBox.style.display = "none";
            return;
        }

        // Cria lista de resultados:
        const resultados = linhas

            // Pega o conteúdo da segunda coluna (índice 1 = nome)
            .map(linha => linha.getElementsByTagName("td")[1].textContent)

            // Filtra apenas os nomes que incluem o termo digitado
            .filter(nome => nome.toLowerCase().includes(termo));

        // Para cada resultado encontrado
        resultados.forEach(nome => {

            // Cria uma div para mostrar a sugestão
            const div = document.createElement("div");

            // Define o texto da sugestão
            div.textContent = nome;

            // Adiciona classe CSS para estilização
            div.classList.add("item-sugestao");

            // Evento ao clicar na sugestão
            div.onclick = function () {

                // Preenche o input com o nome selecionado
                input.value = nome;

                // Limpa sugestões
                sugestoesBox.innerHTML = "";

                // Esconde a caixa de sugestões
                sugestoesBox.style.display = "none";

                // Procura a linha correspondente na tabela
                const linha = linhas.find(
                    l => l.getElementsByTagName("td")[1].textContent === nome
                );

                // Se encontrar a linha
                if (linha) {

                    // Faz scroll suave até a linha
                    linha.scrollIntoView({ behavior: "smooth", block: "center" });

                    // Destaca a linha temporariamente
                    linha.style.backgroundColor = "#ffff99";

                    // Remove o destaque após 1.5 segundos
                    setTimeout(() => linha.style.backgroundColor = "", 1500);
                }
            };

            // Adiciona a sugestão na caixa
            sugestoesBox.appendChild(div);
        });

        // Mostra ou esconde a caixa dependendo se há resultados
        sugestoesBox.style.display = resultados.length > 0 ? "block" : "none";
    });
});