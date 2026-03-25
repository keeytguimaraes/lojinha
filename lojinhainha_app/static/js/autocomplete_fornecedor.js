// autocomplete_fornecedor.js
document.addEventListener("DOMContentLoaded", function() {

    const input = document.getElementById("fornecedor_input");
    const sugestoes = document.getElementById("sugestoes");
    const fornecedores = JSON.parse(input.dataset.fornecedores);

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

            div.onclick = function() {
                input.value = fornecedor.nome_empresa;
                document.getElementById("fornecedor_id").value = fornecedor.id;
                sugestoes.innerHTML = "";
            };

            sugestoes.appendChild(div);
        });
    });

    document.addEventListener("click", function(e) {
        if (!input.contains(e.target) && !sugestoes.contains(e.target)) {
            sugestoes.innerHTML = "";
        }
    });

});