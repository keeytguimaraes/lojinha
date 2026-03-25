// autocomplete_vendedor.js
document.addEventListener("DOMContentLoaded", function() {
    const input = document.getElementById("vendedor_input");
    const sugestoes = document.getElementById("sugestoes");

    const vendedores = JSON.parse(input.dataset.clientes);

    input.addEventListener("input", function() {
        let valor = input.value.toLowerCase();
        sugestoes.innerHTML = "";

        if (valor === "") return;

        let filtrados = vendedores.filter(v =>
            v.nome.toLowerCase().includes(valor)
        );

        filtrados.forEach(vendedor => {
            let div = document.createElement("div");
            div.textContent = vendedor.nome;
            div.classList.add("item-sugestao");

            div.onclick = function() {
                input.value = vendedor.nome;
                document.getElementById("vendedor_id").value = vendedor.id;
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