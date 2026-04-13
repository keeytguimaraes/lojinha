// Espera o carregamento completo do HTML antes de executar o script
document.addEventListener("DOMContentLoaded", function() {

    // Pega o input onde o usuário digita o nome do fornecedor
    const input = document.getElementById("fornecedor_input");

    // Pega a div onde aparecerão as sugestões
    const sugestoes = document.getElementById("sugestoes");

    // Converte o JSON armazenado no data-attribute em um array de objetos
    // Exemplo: data-fornecedores='[{"id":1,"nome_empresa":"Loja X"}]'
    const fornecedores = JSON.parse(input.dataset.fornecedores);

    // Evento disparado sempre que o usuário digita algo no input
    input.addEventListener("input", function() {

        // Pega o valor digitado e transforma em minúsculo
        // Isso evita problemas com letras maiúsculas/minúsculas
        let valor = input.value.toLowerCase();

        // Limpa as sugestões anteriores
        sugestoes.innerHTML = "";

        // Se o campo estiver vazio, não faz nada
        if (valor === "") return;

        // Filtra os fornecedores cujo nome contém o texto digitado
        let filtrados = fornecedores.filter(f =>
            f.nome_empresa.toLowerCase().includes(valor)
        );

        // Para cada fornecedor filtrado, cria uma sugestão na tela
        filtrados.forEach(fornecedor => {

            // Cria uma div para representar a sugestão
            let div = document.createElement("div");

            // Define o texto exibido como o nome da empresa
            div.textContent = fornecedor.nome_empresa;

            // Adiciona uma classe CSS para estilização
            div.classList.add("item-sugestao");

            // Evento de clique na sugestão
            div.onclick = function() {

                // Preenche o input com o nome selecionado
                input.value = fornecedor.nome_empresa;

                // Preenche o campo oculto com o ID do fornecedor
                document.getElementById("fornecedor_id").value = fornecedor.id;

                // Limpa as sugestões após selecionar
                sugestoes.innerHTML = "";
            };

            // Adiciona a sugestão dentro da div de sugestões
            sugestoes.appendChild(div);
        });
    });

    // Evento global para detectar clique fora do autocomplete
    document.addEventListener("click", function(e) {

        // Se o clique não foi no input nem na lista de sugestões
        if (!input.contains(e.target) && !sugestoes.contains(e.target)) {

            // Limpa as sugestões (fecha o autocomplete)
            sugestoes.innerHTML = "";
        }
    });

});