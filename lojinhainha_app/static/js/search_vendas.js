// Espera o carregamento completo do HTML antes de executar o script
// Garante que todos os elementos já estejam disponíveis no DOM
document.addEventListener("DOMContentLoaded", function () {

    // =========================
    // ELEMENTOS PRINCIPAIS
    // =========================

    // Campo de busca onde o usuário digita (input)
    const input = document.getElementById("search-input");

    // Tabela que contém os dados das vendas
    const tabela = document.getElementById("tabela-vendas");

    // Se não existir input ou tabela, interrompe execução
    // Evita erros de referência (null)
    if (!input || !tabela) return;

    // =========================
    // CAPTURA DAS LINHAS DA TABELA
    // =========================

    // Pega todas as linhas da tabela (tr)
    // Array.from → transforma HTMLCollection em array manipulável
    // slice(1) → remove o cabeçalho (primeira linha)
    const linhas = Array.from(tabela.getElementsByTagName("tr")).slice(1);

    // =========================
    // CAIXA DE SUGESTÕES
    // =========================

    // Pega a caixa de sugestões já existente no HTML
    const sugestoesBox = document.getElementById("sugestoes-box");

    // Se não existir a caixa, interrompe o script
    // Diferente de outros códigos, aqui você NÃO cria dinamicamente
    if (!sugestoesBox) return;

    // =========================
    // ESTILIZAÇÃO PADRÃO DA CAIXA
    // =========================
    sugestoesBox.style.position = "absolute";     
    // Permite posicionar livremente na tela

    sugestoesBox.style.background = "white";      
    // Fundo branco para visibilidade

    sugestoesBox.style.border = "1px solid #ccc"; 
    // Borda leve para separar do fundo

    sugestoesBox.style.maxHeight = "150px";       
    // Limita altura máxima da caixa

    sugestoesBox.style.overflowY = "auto";        
    // Adiciona scroll vertical se ultrapassar altura

    sugestoesBox.style.display = "none";          
    // Começa escondida

    sugestoesBox.style.zIndex = "1000";           
    // Garante que fique acima de outros elementos

    // =========================
    // EVENTO DE DIGITAÇÃO
    // =========================
    input.addEventListener("input", function () {

        // Pega o termo digitado e transforma em minúsculo
        const termo = input.value.toLowerCase();

        // Limpa sugestões anteriores
        sugestoesBox.innerHTML = "";

        // Se o campo estiver vazio, esconde a caixa
        if (!termo) {
            sugestoesBox.style.display = "none";
            return;
        }

        // =========================
        // EXTRAÇÃO E FILTRO DOS DADOS
        // =========================
        const resultados = linhas

            // Para cada linha da tabela
            .map(linha => {

                // Segunda coluna (index 1) → nome do cliente
                const cliente = linha.getElementsByTagName("td")[1].textContent;

                // Terceira coluna (index 2) → nome do vendedor
                const vendedor = linha.getElementsByTagName("td")[2].textContent;

                // Retorna um objeto com os dois valores
                return { cliente, vendedor };
            })

            // Filtra resultados onde:
            // - cliente contém o termo OU
            // - vendedor contém o termo
            .filter(item =>
                item.cliente.toLowerCase().includes(termo) ||
                item.vendedor.toLowerCase().includes(termo)
            );

        // =========================
        // CRIAÇÃO DAS SUGESTÕES
        // =========================
        resultados.forEach(item => {

            // Cria uma div para cada sugestão
            const div = document.createElement("div");

            // Exibe cliente + vendedor juntos
            // Ex: "João | Maria"
            div.textContent = item.cliente + " | " + item.vendedor;

            // Classe CSS para estilização (hover, etc)
            div.classList.add("item-sugestao");

            // Define cursor como "clicável"
            div.style.cursor = "pointer";

            // Adiciona espaçamento interno (padding)
            div.style.padding = "5px 10px";

            // =========================
            // EVENTO DE CLIQUE
            // =========================
            div.addEventListener("click", function () {

                // Preenche o input com o nome do cliente
                // (poderia ser vendedor também, dependendo da regra)
                input.value = item.cliente;

                // Limpa sugestões
                sugestoesBox.innerHTML = "";

                // Esconde a caixa
                sugestoesBox.style.display = "none";

                // =========================
                // BUSCA DA LINHA NA TABELA
                // =========================
                const linha = linhas.find(l => {

                    // Pega cliente e vendedor da linha atual
                    const cliente = l.getElementsByTagName("td")[1].textContent;
                    const vendedor = l.getElementsByTagName("td")[2].textContent;

                    // Retorna a linha que tenha os dois valores iguais
                    return cliente === item.cliente && vendedor === item.vendedor;
                });

                // =========================
                // SCROLL + DESTAQUE
                // =========================
                if (linha) {

                    // Faz scroll suave até a linha
                    linha.scrollIntoView({ behavior: "smooth", block: "center" });

                    // Destaca a linha com cor amarela
                    linha.style.backgroundColor = "#ffff99";

                    // Remove o destaque após 1.5 segundos
                    setTimeout(() => linha.style.backgroundColor = "", 1500);
                }
            });

            // Adiciona a sugestão na caixa
            sugestoesBox.appendChild(div);
        });

        // =========================
        // POSICIONAMENTO DINÂMICO
        // =========================
        if (resultados.length > 0) {

            // Obtém posição e tamanho do input
            const rect = input.getBoundingClientRect();

            // Posiciona abaixo do input considerando scroll da página
            sugestoesBox.style.top = rect.bottom + window.scrollY + "px";

            // Alinha à esquerda do input
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

            // Esconde a caixa de sugestões
            sugestoesBox.style.display = "none";
        }
    });
});