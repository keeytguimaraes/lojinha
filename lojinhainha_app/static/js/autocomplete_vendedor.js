// Espera o HTML carregar completamente antes de executar o script
document.addEventListener("DOMContentLoaded", function() {

    // Pega o campo de input onde o usuário digita o nome do vendedor
    const input = document.getElementById("vendedor_input");

    // Pega a div onde serão exibidas as sugestões
    const sugestoes = document.getElementById("sugestoes");

    // Converte o JSON armazenado no data-attribute em um array de objetos
    //  Aqui você usou "clientes", mas na prática são vendedores
    const vendedores = JSON.parse(input.dataset.clientes);

    // Evento disparado sempre que o usuário digita algo
    input.addEventListener("input", function() {

        // Pega o valor digitado e transforma em minúsculo
        let valor = input.value.toLowerCase();

        // Limpa sugestões anteriores
        sugestoes.innerHTML = "";

        // Se o campo estiver vazio, não faz nada
        if (valor === "") return;

        // Filtra os vendedores cujo nome contém o texto digitado
        let filtrados = vendedores.filter(v =>
            v.nome.toLowerCase().includes(valor)
        );

        // Para cada vendedor filtrado, cria uma sugestão
        filtrados.forEach(vendedor => {

            // Cria uma div para representar a sugestão
            let div = document.createElement("div");

            // Define o texto da sugestão como o nome do vendedor
            div.textContent = vendedor.nome;

            // Adiciona classe CSS para estilização
            div.classList.add("item-sugestao");

            // Evento ao clicar na sugestão
            div.onclick = function() {

                // Preenche o input com o nome selecionado
                input.value = vendedor.nome;

                // Preenche o campo oculto com o ID do vendedor
                document.getElementById("vendedor_id").value = vendedor.id;

                // Limpa as sugestões
                sugestoes.innerHTML = "";
            };

            // Adiciona a sugestão na tela
            sugestoes.appendChild(div);
        });
    });

    // Evento global para detectar clique fora do autocomplete
    document.addEventListener("click", function(e) {

        // Se o clique não foi dentro do input nem da lista de sugestões
        if (!input.contains(e.target) && !sugestoes.contains(e.target)) {

            // Limpa as sugestões (fecha o autocomplete)
            sugestoes.innerHTML = "";
        }
    });
});