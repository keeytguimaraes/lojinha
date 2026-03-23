// autocomplete_cliente.js
document.addEventListener("DOMContentLoaded", function() {
    const input = document.getElementById("cliente_input");
    const sugestoes = document.getElementById("sugestoes");
    const clientes = JSON.parse(input.dataset.clientes); // pegamos os clientes do data-attribute

    input.addEventListener("input", function() {
        let valor = input.value.toLowerCase();
        sugestoes.innerHTML = "";

        if (valor === "") return;

        let filtrados = clientes.filter(c =>
            c.nome.toLowerCase().includes(valor)
        );

        filtrados.forEach(cliente => {
            let div = document.createElement("div");
            div.textContent = cliente.nome;
            div.classList.add("item-sugestao");

            div.onclick = function() {
                input.value = cliente.nome;
                document.getElementById("cliente_id").value = cliente.id;
                document.getElementById("cpf").value = cliente.cpf;
                sugestoes.innerHTML = "";
            };

            sugestoes.appendChild(div);
        });
    });

    // opcional: fechar sugestões ao clicar fora
    document.addEventListener("click", function(e) {
        if (!input.contains(e.target) && !sugestoes.contains(e.target)) {
            sugestoes.innerHTML = "";
        }
    });
});