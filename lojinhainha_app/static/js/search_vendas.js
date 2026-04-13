// Espera o carregamento completo do HTML antes de executar o script
document.addEventListener("DOMContentLoaded", function () {

    // Campo de busca
    const input = document.getElementById("search-input");

    // Tabela de vendas
    const tabela = document.getElementById("tabela-vendas");

    // Se não existir input ou tabela, interrompe execução (evita erro)
    if (!input || !tabela) return;

    // Pega todas as linhas da tabela (ignorando o cabeçalho)
    const linhas = Array.from(tabela.getElementsByTagName("tr")).slice(1);

    // Pega a caixa de sugestões já existente
    const sugestoesBox = document.getElementById("sugestoes-box");

    // Se não existir a caixa, interrompe (diferente dos outros scripts, aqui você não cria)
    if (!sugestoesBox) return;

    //  DEFINE ESTILOS PADRÃO (mesmo comportamento dos outros módulos)
    sugestoesBox.style.position = "absolute";     // Permite posicionamento livre
    sugestoesBox.style.background = "white";      // Fundo branco
    sugestoesBox.style.border = "1px solid #ccc"; // Borda leve
    sugestoesBox.style.maxHeight = "150px";       // Altura máxima
    sugestoesBox.style.overflowY = "auto";        // Scroll vertical
    sugestoesBox.style.display = "none";          // Começa escondido
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

        //  GERA RESULTADOS USANDO DUAS COLUNAS (cliente e vendedor)
        const resultados = linhas

            // Para cada linha, extrai cliente e vendedor
            .map(linha => {

                // Segunda coluna → nome do cliente
                const cliente = linha.getElementsByTagName("td")[1].textContent;

                // Terceira coluna → nome do vendedor
                const vendedor = linha.getElementsByTagName("td")[2].textContent;

                // Retorna objeto com ambos os dados
                return { cliente, vendedor };
            })

            // Filtra se o termo estiver em cliente OU vendedor
            .filter(item =>
                item.cliente.toLowerCase().includes(termo) ||
                item.vendedor.toLowerCase().includes(termo)
            );

        // Para cada resultado encontrado
        resultados.forEach(item => {

            // Cria uma div para sugestão
            const div = document.createElement("div");

            // Mostra cliente e vendedor juntos
            div.textContent = item.cliente + " | " + item.vendedor;

            // Adiciona classe CSS
            div.classList.add("item-sugestao");

            // Define cursor como clicável
            div.style.cursor = "pointer";

            // Adiciona espaçamento interno
            div.style.padding = "5px 10px";

            // Evento ao clicar na sugestão
            div.addEventListener("click", function () {

                // Preenche o input com o cliente (poderia ser vendedor também)
                input.value = item.cliente;

                // Limpa sugestões
                sugestoesBox.innerHTML = "";

                // Esconde a caixa
                sugestoesBox.style.display = "none";

                // Procura a linha correspondente usando cliente E vendedor
                const linha = linhas.find(l => {

                    const cliente = l.getElementsByTagName("td")[1].textContent;
                    const vendedor = l.getElementsByTagName("td")[2].textContent;

                    // Só retorna a linha se ambos baterem
                    return cliente === item.cliente && vendedor === item.vendedor;
                });

                // Se encontrar a linha
                if (linha) {

                    // Scroll suave até ela
                    linha.scrollIntoView({ behavior: "smooth", block: "center" });

                    // Destaca a linha
                    linha.style.backgroundColor = "#ffff99";

                    // Remove destaque após 1.5 segundos
                    setTimeout(() => linha.style.backgroundColor = "", 1500);
                }
            });

            // Adiciona a sugestão na caixa
            sugestoesBox.appendChild(div);
        });

        //  POSICIONAMENTO DINÂMICO (igual aos outros módulos)
        if (resultados.length > 0) {

            // Pega posição do input
            const rect = input.getBoundingClientRect();

            // Posiciona abaixo do input considerando scroll
            sugestoesBox.style.top = rect.bottom + window.scrollY + "px";

            // Alinha à esquerda
            sugestoesBox.style.left = rect.left + window.scrollX + "px";

            // Define mesma largura
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

        // Se clicou fora do input e da caixa
        if (e.target !== input && !sugestoesBox.contains(e.target)) {

            // Esconde sugestões
            sugestoesBox.style.display = "none";
        }
    });
});