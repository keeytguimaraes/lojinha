// Espera o carregamento completo do HTML antes de executar o script
// Isso garante que os elementos existam antes de serem manipulados
document.addEventListener("DOMContentLoaded", function() {

    // Pega o input onde o usuário digita o nome do fornecedor
    // Esse elemento deve existir no HTML com id="fornecedor_input"
    const input = document.getElementById("fornecedor_input");

    // Pega a div onde aparecerão as sugestões de autocomplete
    // Essa div será preenchida dinamicamente com os resultados filtrados
    const sugestoes = document.getElementById("sugestoes");

    // Converte o JSON armazenado no data-attribute em um array de objetos
    // input.dataset.fornecedores → acessa o atributo data-fornecedores=""
    // JSON.parse → transforma string JSON em array JavaScript
    // Exemplo no HTML:
    // <input data-fornecedores='[{"id":1,"nome_empresa":"Loja X"}]'>
    const fornecedores = JSON.parse(input.dataset.fornecedores);

    // Evento disparado sempre que o usuário digita algo no input
    input.addEventListener("input", function() {

        // Pega o valor digitado e transforma em minúsculo
        // Isso evita problemas de comparação entre maiúsculas/minúsculas
        let valor = input.value.toLowerCase();

        // Limpa as sugestões anteriores (evita duplicação visual)
        sugestoes.innerHTML = "";

        // Se o campo estiver vazio, não executa o filtro
        // Evita mostrar todos os fornecedores sem necessidade
        if (valor === "") return;

        // Filtra os fornecedores cujo nome contém o texto digitado
        // filter → percorre o array e retorna apenas os que atendem a condição
        // includes → verifica se o texto digitado está contido no nome
        let filtrados = fornecedores.filter(f =>
            f.nome_empresa.toLowerCase().includes(valor)
        );

        // Para cada fornecedor filtrado, cria uma sugestão na tela
        filtrados.forEach(fornecedor => {

            // Cria uma nova div para representar uma sugestão
            let div = document.createElement("div");

            // Define o texto exibido como o nome da empresa fornecedora
            div.textContent = fornecedor.nome_empresa;

            // Adiciona uma classe CSS para estilização (ex: hover, destaque, etc)
            div.classList.add("item-sugestao");

            // Evento de clique na sugestão
            // Quando o usuário clicar, os dados são preenchidos automaticamente
            div.onclick = function() {

                // Preenche o input principal com o nome selecionado
                input.value = fornecedor.nome_empresa;

                // Preenche um campo oculto com o ID do fornecedor
                // Esse ID será enviado ao backend para identificar corretamente o registro
                document.getElementById("fornecedor_id").value = fornecedor.id;

                // Limpa a lista de sugestões após a seleção
                sugestoes.innerHTML = "";
            };

            // Adiciona a sugestão criada dentro da div de sugestões
            sugestoes.appendChild(div);
        });
    });

    // Evento global para detectar clique fora do autocomplete
    document.addEventListener("click", function(e) {

        // Verifica se o clique NÃO foi dentro:
        // - do input
        // - nem da lista de sugestões
        if (!input.contains(e.target) && !sugestoes.contains(e.target)) {

            // Limpa as sugestões (fecha o autocomplete)
            sugestoes.innerHTML = "";
        }
    });

});