document.addEventListener("DOMContentLoaded", function () {
    // Espera todo o HTML carregar antes de executar o script
    // Evita erros como "elemento não encontrado"

    // =========================
    // MENU LATERAL
    // =========================
    window.toggleMenu = function () {
        // Cria uma função global (fica disponível no escopo window)
        // Pode ser chamada direto no HTML, por exemplo: onclick="toggleMenu()"

        var sidebar = document.getElementById("sidebar");
        // Seleciona o elemento da barra lateral (menu)

        var content = document.getElementById("content");
        // Seleciona o conteúdo principal da página

        if (sidebar && content) {
            // Verifica se ambos os elementos existem no DOM
            // Evita erro caso algum ID não esteja presente na página

            sidebar.classList.toggle("active");
            // Alterna (adiciona/remove) a classe "active" na sidebar
            // Normalmente usada para abrir/fechar o menu lateral via CSS

            content.classList.toggle("shift");
            // Alterna a classe "shift" no conteúdo principal
            // Geralmente empurra o conteúdo quando o menu abre
        }
    };

    // =========================
    // CONTROLE DE PREÇO (CASAS DECIMAIS)
    // =========================
    var camposPreco = document.querySelectorAll('input[name="preco"], input[name="preco_venda"]');
    // Seleciona todos os inputs que tenham:
    // name="preco" OU name="preco_venda"
    // Retorna uma NodeList (lista de elementos)

    camposPreco.forEach(function(input) {
        // Percorre cada campo de preço encontrado

        input.addEventListener("input", function () {
            // Evento disparado sempre que o usuário digita algo no campo

            var valor = this.value;
            // Pega o valor atual digitado no input

            if (valor.indexOf(".") !== -1) {
                // Verifica se existe ponto decimal (".")
                // indexOf retorna -1 se não encontrar

                var partes = valor.split(".");
                // Divide o valor em duas partes:
                // partes[0] → antes do ponto (inteiro)
                // partes[1] → depois do ponto (decimal)

                partes[1] = partes[1].slice(0, 2);
                // Limita a parte decimal para no máximo 2 casas
                // slice(0, 2) pega apenas os dois primeiros caracteres

                this.value = partes[0] + "." + partes[1];
                // Reconstrói o valor juntando inteiro + "." + decimal limitado
            }
        });
    });

    // =========================
    // VALIDAÇÃO DE CPF
    // =========================
    var camposCpf = document.querySelectorAll('input[name="cpf"]');
    // Seleciona todos os inputs com name="cpf"

    camposCpf.forEach(function(input) {
        // Percorre todos os campos de CPF

        input.addEventListener("input", function () {
            // Evento disparado ao digitar

            this.value = this.value.replace(/\D/g, "");
            // Remove tudo que NÃO for número
            // \D → qualquer caractere não numérico
            // g → aplica para todos os caracteres

            this.value = this.value.slice(0, 11);
            // Limita o valor a no máximo 11 dígitos (tamanho do CPF)
        });
    });

    // =========================
    // VALIDAÇÃO DE CNPJ
    // =========================
    var camposCnpj = document.querySelectorAll('input[name="cnpj"]');
    // Seleciona todos os inputs com name="cnpj"

    camposCnpj.forEach(function(input) {
        // Percorre todos os campos de CNPJ

        input.addEventListener("input", function () {
            // Evento disparado ao digitar

            this.value = this.value.replace(/\D/g, "");
            // Remove qualquer caractere que não seja número

            this.value = this.value.slice(0, 14);
            // Limita o valor a no máximo 14 dígitos (tamanho do CNPJ)
        });
    });

});