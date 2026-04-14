// Espera o HTML carregar completamente antes de executar o script
// Isso evita erros como "elemento não encontrado"
document.addEventListener("DOMContentLoaded", function() {

    // Pega o input onde o usuário digita o nome do cliente
    // Esse input deve existir no HTML com id="cliente_input"
    const input = document.getElementById("cliente_input");

    // Pega a div onde vão aparecer as sugestões de autocomplete
    // Essa div será preenchida dinamicamente com os resultados
    const sugestoes = document.getElementById("sugestoes");

    // Converte o JSON armazenado no atributo data-clientes do input
    // dataset.clientes → acessa o atributo HTML data-clientes=""
    // JSON.parse → transforma string JSON em objeto/array JavaScript
    // Exemplo no HTML:
    // <input data-clientes='[{"id":1,"nome":"Ana","cpf":"123"}]'>
    const clientes = JSON.parse(input.dataset.clientes);

    // Evento que dispara toda vez que o usuário digita algo no input
    input.addEventListener("input", function() {

        // Pega o valor digitado e transforma em minúsculo
        // Isso evita erro de comparação (ex: "Ana" vs "ana")
        let valor = input.value.toLowerCase();

        // Limpa as sugestões anteriores (evita duplicação)
        sugestoes.innerHTML = "";

        // Se o campo estiver vazio, não faz nada (evita mostrar lista inteira)
        if (valor === "") return;

        // Filtra os clientes cujo nome contém o texto digitado
        // filter → percorre o array e retorna apenas os que atendem a condição
        // includes → verifica se o texto digitado está dentro do nome
        let filtrados = clientes.filter(c =>
            c.nome.toLowerCase().includes(valor)
        );

        // Para cada cliente filtrado, cria uma sugestão na tela
        filtrados.forEach(cliente => {

            // Cria uma nova div para representar uma sugestão
            let div = document.createElement("div");

            // Define o texto visível como o nome do cliente
            div.textContent = cliente.nome;

            // Adiciona uma classe CSS para estilização (ex: hover, cor, etc)
            div.classList.add("item-sugestao");

            // Evento de clique na sugestão
            // Quando o usuário clicar, os dados são preenchidos automaticamente
            div.onclick = function() {

                // Preenche o input principal com o nome escolhido
                input.value = cliente.nome;

                // Preenche o campo oculto com o ID do cliente
                // Esse ID é usado no backend (banco de dados)
                document.getElementById("cliente_id").value = cliente.id;

                // Preenche automaticamente o CPF do cliente
                document.getElementById("cpf").value = cliente.cpf;

                // Limpa a lista de sugestões após a seleção
                sugestoes.innerHTML = "";
            };

            // Adiciona a div criada dentro da área de sugestões
            sugestoes.appendChild(div);
        });
    });

    // Evento global para detectar cliques fora do input ou da lista
    document.addEventListener("click", function(e) {

        // Verifica se o clique NÃO foi dentro:
        // - do input
        // - nem da área de sugestões
        if (!input.contains(e.target) && !sugestoes.contains(e.target)) {

            // Limpa as sugestões (fecha o autocomplete)
            sugestoes.innerHTML = "";
        }
    });
});