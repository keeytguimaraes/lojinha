// Adiciona um "ouvinte de evento" ao documento inteiro
// "DOMContentLoaded" garante que o código só será executado
// depois que TODO o HTML da página for carregado
document.addEventListener("DOMContentLoaded", function() {

    // Seleciona o campo de input onde o usuário digita o nome do vendedor
    // getElementById busca um elemento pelo id no HTML
    const input = document.getElementById("vendedor_input");

    // Seleciona a div onde as sugestões de vendedores serão exibidas
    const sugestoes = document.getElementById("sugestoes");

    // Acessa um atributo personalizado "data-clientes" do input (data-attribute)
    // dataset.clientes retorna esse valor como STRING
    // JSON.parse converte essa string JSON em um ARRAY de objetos JavaScript
    // Ex: [{id: 1, nome: "João"}, {id: 2, nome: "Maria"}]
    // OBS: apesar do nome "clientes", aqui estão sendo usados como vendedores
    const vendedores = JSON.parse(input.dataset.clientes);

    // Adiciona um evento ao input que dispara toda vez que o usuário digita algo
    input.addEventListener("input", function() {

        // Pega o valor atual digitado no input
        // toLowerCase() transforma tudo em minúsculo para facilitar a comparação
        // (evita diferença entre maiúsculas/minúsculas)
        let valor = input.value.toLowerCase();

        // Limpa qualquer sugestão exibida anteriormente
        // innerHTML = "" remove todo o conteúdo interno da div
        sugestoes.innerHTML = "";

        // Se o campo estiver vazio, interrompe a execução da função
        // "return" aqui evita processamento desnecessário
        if (valor === "") return;

        // Filtra o array de vendedores
        // filter percorre todos os vendedores e retorna apenas os que atendem a condição
        let filtrados = vendedores.filter(v =>

            // Para cada vendedor:
            // - Converte o nome para minúsculo
            // - Verifica se contém o texto digitado (includes)
            v.nome.toLowerCase().includes(valor)
        );

        // Para cada vendedor que passou no filtro
        filtrados.forEach(vendedor => {

            // Cria dinamicamente uma nova <div> no HTML
            let div = document.createElement("div");

            // Define o texto da div como o nome do vendedor
            // textContent insere texto puro (sem HTML)
            div.textContent = vendedor.nome;

            // Adiciona uma classe CSS chamada "item-sugestao"
            // Isso permite estilizar cada sugestão via CSS
            div.classList.add("item-sugestao");

            // Define o que acontece quando o usuário clicar em uma sugestão
            div.onclick = function() {

                // Preenche o input com o nome do vendedor selecionado
                input.value = vendedor.nome;

                // Define o valor de um campo oculto (hidden)
                // Isso é útil para enviar o ID real do vendedor para o backend
                document.getElementById("vendedor_id").value = vendedor.id;

                // Limpa as sugestões após a seleção
                sugestoes.innerHTML = "";
            };

            // Adiciona a div criada dentro da div de sugestões
            // appendChild insere o elemento como "filho"
            sugestoes.appendChild(div);
        });
    });

    // Adiciona um evento global de clique no documento inteiro
    document.addEventListener("click", function(e) {

        // Verifica se o clique NÃO foi dentro do input
        // E também NÃO foi dentro da div de sugestões
        // contains() verifica se o elemento clicado está dentro do elemento
        if (!input.contains(e.target) && !sugestoes.contains(e.target)) {

            // Se clicou fora, limpa as sugestões (fecha o autocomplete)
            sugestoes.innerHTML = "";
        }
    });
});