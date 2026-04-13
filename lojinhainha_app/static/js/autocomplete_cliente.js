// Espera o HTML carregar completamente antes de executar o script
document.addEventListener("DOMContentLoaded", function() {

    // Pega o input onde o usuário digita o nome do cliente
    const input = document.getElementById("cliente_input");

    // Pega a div onde vão aparecer as sugestões
    const sugestoes = document.getElementById("sugestoes");

    // Converte o JSON armazenado no data-attribute do input em um array de objetos
    // Exemplo: data-clientes='[{"id":1,"nome":"Ana","cpf":"123"}]'
    const clientes = JSON.parse(input.dataset.clientes);

    // Evento que dispara toda vez que o usuário digita algo
    input.addEventListener("input", function() {

        // Pega o valor digitado e transforma em minúsculo (para evitar problemas de comparação)
        let valor = input.value.toLowerCase();

        // Limpa as sugestões anteriores
        sugestoes.innerHTML = "";

        // Se o campo estiver vazio, não faz nada
        if (valor === "") return;

        // Filtra os clientes cujo nome contém o texto digitado
        let filtrados = clientes.filter(c =>
            c.nome.toLowerCase().includes(valor)
        );

        // Para cada cliente filtrado, cria uma sugestão na tela
        filtrados.forEach(cliente => {

            // Cria uma div para representar a sugestão
            let div = document.createElement("div");

            // Define o texto da sugestão como o nome do cliente
            div.textContent = cliente.nome;

            // Adiciona uma classe CSS para estilização
            div.classList.add("item-sugestao");

            // Evento de clique na sugestão
            div.onclick = function() {

                // Preenche o input com o nome selecionado
                input.value = cliente.nome;

                // Preenche o campo oculto com o ID do cliente (usado no backend)
                document.getElementById("cliente_id").value = cliente.id;

                // Preenche automaticamente o CPF do cliente
                document.getElementById("cpf").value = cliente.cpf;

                // Limpa a lista de sugestões após seleção
                sugestoes.innerHTML = "";
            };

            // Adiciona a sugestão dentro da div de sugestões
            sugestoes.appendChild(div);
        });
    });

    // Evento global para detectar cliques fora do input/sugestões
    document.addEventListener("click", function(e) {

        // Se o clique NÃO foi dentro do input nem da lista de sugestões
        if (!input.contains(e.target) && !sugestoes.contains(e.target)) {

            // Limpa as sugestões (fecha o autocomplete)
            sugestoes.innerHTML = "";
        }
    });
});