// Espera o carregamento completo do HTML antes de executar o script
// Garante que todos os elementos já existam no DOM antes de serem usados
document.addEventListener("DOMContentLoaded", function() {

    // Campo onde o usuário digita o fornecedor
    // Esse input deve existir no HTML com id="fornecedor_input"
    const input = document.getElementById("fornecedor_input");

    // Campo oculto que armazena o ID do fornecedor
    // Esse valor é enviado ao backend (não visível para o usuário)
    const hidden = document.getElementById("fornecedor_id");

    // Div onde aparecem as sugestões de autocomplete
    // Será preenchida dinamicamente conforme o usuário digita
    const sugestoes = document.getElementById("sugestoes_fornecedor");

    // Converte o JSON armazenado no atributo data-fornecedores
    // dataset.fornecedores → acessa o atributo data-fornecedores=""
    // JSON.parse → transforma string JSON em array de objetos JavaScript
    const fornecedores = JSON.parse(input.dataset.fornecedores);

    // Campo de quantidade digitada pelo usuário
    // Usado para calcular o preço total
    const quantidadeInput = document.getElementById("quantidade");

    // Campo que exibirá o preço unitário calculado (com lucro)
    const precoUnitarioInput = document.getElementById("preco_unitario");

    // Campo que exibirá o preço total da venda
    const precoTotalInput = document.getElementById("preco_total");

    // =========================
    // FUNÇÃO DE CÁLCULO DE PREÇO
    // =========================
    function calcularPreco() {

        // Pega o ID do fornecedor selecionado (campo oculto)
        let fornecedor_id = hidden.value;

        // Converte a quantidade digitada para número decimal
        // parseFloat permite valores como "2.5"
        let quantidade = parseFloat(quantidadeInput.value);

        // Validação:
        // Se não tiver fornecedor selecionado OU quantidade inválida
        if (!fornecedor_id || quantidade <= 0) {
            // Limpa os campos de preço para evitar valores incorretos
            precoUnitarioInput.value = "";
            precoTotalInput.value = "";
            return; // interrompe a execução da função
        }

        // Faz requisição ao backend para buscar o preço real do fornecedor
        // Isso evita manipulação de valores no front-end (mais seguro)
        fetch(`/get_preco_fornecedor/${fornecedor_id}`)

            // Converte a resposta HTTP para JSON
            .then(response => response.json())

            // Processa os dados retornados pelo backend
            .then(data => {

                // Converte o preço recebido para número
                let precoFornecedor = parseFloat(data.preco);

                // Aplica margem de lucro de 20%
                let precoUnitario = precoFornecedor * 1.2;

                // Calcula o preço total baseado na quantidade
                let precoTotal = precoUnitario * quantidade;

                // Atualiza os campos no formulário
                // toFixed(2) → limita a 2 casas decimais (padrão monetário)
                precoUnitarioInput.value = precoUnitario.toFixed(2);
                precoTotalInput.value = precoTotal.toFixed(2);
            });
    }

    // =========================
    // AUTOCOMPLETE DE FORNECEDORES
    // =========================
    input.addEventListener("input", function() {

        // Pega o valor digitado e transforma em minúsculo
        // Evita problemas com comparação de maiúsculas/minúsculas
        let valor = input.value.toLowerCase();

        // Limpa sugestões anteriores (evita duplicação)
        sugestoes.innerHTML = "";

        // Se o campo estiver vazio, não faz nada
        if (valor === "") return;

        // Filtra os fornecedores cujo nome contém o texto digitado
        let filtrados = fornecedores.filter(f =>
            f.nome_empresa.toLowerCase().includes(valor)
        );

        // Para cada fornecedor filtrado, cria uma sugestão
        filtrados.forEach(fornecedor => {

            // Cria uma div para representar a sugestão
            let div = document.createElement("div");

            // Define o texto exibido
            div.textContent = fornecedor.nome_empresa;

            // Adiciona classe CSS para estilização
            div.classList.add("item-sugestao");

            // Evento ao clicar na sugestão
            div.addEventListener("click", function() {

                // Preenche o input com o nome do fornecedor selecionado
                input.value = fornecedor.nome_empresa;

                // Armazena o ID do fornecedor no campo oculto
                hidden.value = fornecedor.id;

                // Limpa a lista de sugestões
                sugestoes.innerHTML = "";

                // Recalcula o preço automaticamente após seleção
                calcularPreco();
            });

            // Adiciona a sugestão na tela
            sugestoes.appendChild(div);
        });
    });

    // =========================
    // FECHAR AUTOCOMPLETE AO CLICAR FORA
    // =========================
    document.addEventListener("click", function(e) {

        // Verifica se o clique NÃO foi dentro:
        // - do input
        // - nem da área de sugestões
        if (!input.contains(e.target) && !sugestoes.contains(e.target)) {

            // Limpa as sugestões (fecha autocomplete)
            sugestoes.innerHTML = "";
        }
    });

    // =========================
    // RECÁLCULO AUTOMÁTICO
    // =========================
    // Sempre que o usuário altera a quantidade, recalcula o preço
    quantidadeInput.addEventListener("input", calcularPreco);

});