document.addEventListener("DOMContentLoaded", function() {

    const input = document.getElementById("fornecedor_input");
    const hidden = document.getElementById("fornecedor_id");
    const sugestoes = document.getElementById("sugestoes_fornecedor");
    const fornecedores = JSON.parse(input.dataset.fornecedores);
    const quantidadeInput = document.getElementById("quantidade");
    const precoUnitarioInput = document.getElementById("preco_unitario");
    const precoTotalInput = document.getElementById("preco_total");

    // Função para calcular preço
    function calcularPreco() {
        let fornecedor_id = hidden.value;
        let quantidade = parseFloat(quantidadeInput.value);

        if (!fornecedor_id || quantidade <= 0) {
            precoUnitarioInput.value = "";
            precoTotalInput.value = "";
            return;
        }

        fetch(`/get_preco_fornecedor/${fornecedor_id}`)
            .then(response => response.json())
            .then(data => {
                let precoFornecedor = parseFloat(data.preco);

                let precoUnitario = precoFornecedor * 1.2;
                let precoTotal = precoUnitario * quantidade;

                precoUnitarioInput.value = precoUnitario.toFixed(2);
                precoTotalInput.value = precoTotal.toFixed(2);
            });
    }

    // Autocomplete fornecedores
    input.addEventListener("input", function() {
        let valor = input.value.toLowerCase();
        sugestoes.innerHTML = "";

        if (valor === "") return;

        let filtrados = fornecedores.filter(f =>
            f.nome_empresa.toLowerCase().includes(valor)
        );

        filtrados.forEach(fornecedor => {
            let div = document.createElement("div");
            div.textContent = fornecedor.nome_empresa;
            div.classList.add("item-sugestao");

            div.addEventListener("click", function() {
                input.value = fornecedor.nome_empresa;
                hidden.value = fornecedor.id;
                sugestoes.innerHTML = "";

                calcularPreco(); // recalcula após selecionar fornecedor
            });

            sugestoes.appendChild(div);
        });
    });

    // Fecha sugestões ao clicar fora
    document.addEventListener("click", function(e) {
        if (!input.contains(e.target) && !sugestoes.contains(e.target)) {
            sugestoes.innerHTML = "";
        }
    });

    // Recalcula preço quando a quantidade muda
    quantidadeInput.addEventListener("input", calcularPreco);

});