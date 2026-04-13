// Espera o carregamento completo do HTML antes de executar o script
document.addEventListener("DOMContentLoaded", function() {

    // Campo onde o usuário digita o fornecedor
    const input = document.getElementById("fornecedor_input");

    // Campo oculto que armazena o ID do fornecedor (usado no backend)
    const hidden = document.getElementById("fornecedor_id");

    // Div onde aparecem as sugestões de autocomplete
    const sugestoes = document.getElementById("sugestoes_fornecedor");

    // Converte o JSON do data-attribute em array de objetos
    const fornecedores = JSON.parse(input.dataset.fornecedores);

    // Campo de quantidade digitada pelo usuário
    const quantidadeInput = document.getElementById("quantidade");

    // Campo que exibirá o preço unitário calculado
    const precoUnitarioInput = document.getElementById("preco_unitario");

    // Campo que exibirá o preço total calculado
    const precoTotalInput = document.getElementById("preco_total");

    // Função responsável por calcular os preços
    function calcularPreco() {

        // Pega o ID do fornecedor selecionado
        let fornecedor_id = hidden.value;

        // Converte a quantidade para número decimal
        let quantidade = parseFloat(quantidadeInput.value);

        // Se não tiver fornecedor ou quantidade inválida, limpa os campos
        if (!fornecedor_id || quantidade <= 0) {
            precoUnitarioInput.value = "";
            precoTotalInput.value = "";
            return;
        }

        // Faz requisição ao backend para buscar o preço real do fornecedor
        fetch(`/get_preco_fornecedor/${fornecedor_id}`)

            // Converte a resposta para JSON
            .then(response => response.json())

            // Processa os dados retornados
            .then(data => {

                // Converte o preço recebido para número
                let precoFornecedor = parseFloat(data.preco);

                // Calcula preço com margem de lucro (20%)
                let precoUnitario = precoFornecedor * 1.2;

                // Calcula preço total baseado na quantidade
                let precoTotal = precoUnitario * quantidade;

                // Atualiza os campos no formulário com 2 casas decimais
                precoUnitarioInput.value = precoUnitario.toFixed(2);
                precoTotalInput.value = precoTotal.toFixed(2);
            });
    }

    // Autocomplete de fornecedores
    input.addEventListener("input", function() {

        // Pega o valor digitado e transforma em minúsculo
        let valor = input.value.toLowerCase();

        // Limpa sugestões anteriores
        sugestoes.innerHTML = "";

        // Se estiver vazio, não faz nada
        if (valor === "") return;

        // Filtra fornecedores pelo nome
        let filtrados = fornecedores.filter(f =>
            f.nome_empresa.toLowerCase().includes(valor)
        );

        // Cria uma sugestão para cada fornecedor filtrado
        filtrados.forEach(fornecedor => {

            // Cria uma div para a sugestão
            let div = document.createElement("div");

            // Define o texto da sugestão
            div.textContent = fornecedor.nome_empresa;

            // Adiciona classe CSS
            div.classList.add("item-sugestao");

            // Evento ao clicar na sugestão
            div.addEventListener("click", function() {

                // Preenche o input com o nome do fornecedor
                input.value = fornecedor.nome_empresa;

                // Salva o ID no campo oculto
                hidden.value = fornecedor.id;

                // Limpa sugestões
                sugestoes.innerHTML = "";

                // Recalcula o preço após selecionar fornecedor
                calcularPreco();
            });

            // Adiciona a sugestão na tela
            sugestoes.appendChild(div);
        });
    });

    // Fecha sugestões ao clicar fora
    document.addEventListener("click", function(e) {

        // Se o clique não foi no input nem nas sugestões
        if (!input.contains(e.target) && !sugestoes.contains(e.target)) {

            // Limpa as sugestões
            sugestoes.innerHTML = "";
        }
    });

    // Recalcula o preço sempre que a quantidade mudar
    quantidadeInput.addEventListener("input", calcularPreco);

});