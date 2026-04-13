document.addEventListener("DOMContentLoaded", function () {
    // Espera todo o HTML carregar antes de executar o script

    // MENU LATERAL
    window.toggleMenu = function () {
        // Cria uma função global (pode ser chamada no HTML, tipo onclick)

        var sidebar = document.getElementById("sidebar");
        // Pega o elemento da barra lateral

        var content = document.getElementById("content");
        // Pega o conteúdo principal da página

        if (sidebar && content) {
            // Verifica se os dois elementos existem

            sidebar.classList.toggle("active");
            // Adiciona ou remove a classe "active" na sidebar (abre/fecha menu)

            content.classList.toggle("shift");
            // Move o conteúdo principal (geralmente empurra quando o menu abre)
        }
    };

    // PREÇO 
    var camposPreco = document.querySelectorAll('input[name="preco"], input[name="preco_venda"]');
    // Seleciona todos os inputs que tenham name "preco" ou "preco_venda"

    camposPreco.forEach(function(input) {
        // Para cada campo de preço encontrado

        input.addEventListener("input", function () {
            // Evento que dispara quando o usuário digita

            var valor = this.value;
            // Pega o valor digitado

            if (valor.indexOf(".") !== -1) {
                // Verifica se existe ponto decimal

                var partes = valor.split(".");
                // Divide o valor em duas partes (antes e depois do ponto)

                partes[1] = partes[1].slice(0, 2);
                // Limita a parte decimal para no máximo 2 casas

                this.value = partes[0] + "." + partes[1];
                // Reconstrói o valor com apenas 2 casas decimais
            }
        });
    });

    // CPF
    var camposCpf = document.querySelectorAll('input[name="cpf"]');
    // Seleciona todos os campos de CPF

    camposCpf.forEach(function(input) {
        // Para cada campo de CPF

        input.addEventListener("input", function () {
            // Evento ao digitar

            this.value = this.value.replace(/\D/g, "");
            // Remove tudo que NÃO for número (letras, símbolos, etc)

            this.value = this.value.slice(0, 11);
            // Limita o CPF a 11 dígitos
        });
    });

    // CNPJ
    var camposCnpj = document.querySelectorAll('input[name="cnpj"]');
    // Seleciona todos os campos de CNPJ

    camposCnpj.forEach(function(input) {
        // Para cada campo de CNPJ

        input.addEventListener("input", function () {
            // Evento ao digitar

            this.value = this.value.replace(/\D/g, "");
            // Remove tudo que não for número

            this.value = this.value.slice(0, 14);
            // Limita o CNPJ a 14 dígitos
        });
    });

});