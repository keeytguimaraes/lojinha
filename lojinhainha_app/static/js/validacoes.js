document.addEventListener("DOMContentLoaded", function () {

    // MENU LATERAL
    window.toggleMenu = function () {
        var sidebar = document.getElementById("sidebar");
        var content = document.getElementById("content");

        if (sidebar && content) {
            sidebar.classList.toggle("active");
            content.classList.toggle("shift");
            
        }
    };

    // PREÇO
    var camposPreco = document.querySelectorAll('input[name="preco"], input[name="preco_venda"]');

    camposPreco.forEach(function(input) {
        input.addEventListener("input", function () {
            var valor = this.value;

            if (valor.indexOf(".") !== -1) {
                var partes = valor.split(".");
                partes[1] = partes[1].slice(0, 2);
                this.value = partes[0] + "." + partes[1];
            }
        });
    });

    // CPF
    var camposCpf = document.querySelectorAll('input[name="cpf"]');

    camposCpf.forEach(function(input) {
        input.addEventListener("input", function () {
            this.value = this.value.replace(/\D/g, "");
            this.value = this.value.slice(0, 11);
        });
    });

    // CNPJ
    var camposCnpj = document.querySelectorAll('input[name="cnpj"]');

    camposCnpj.forEach(function(input) {
        input.addEventListener("input", function () {
            this.value = this.value.replace(/\D/g, "");
            this.value = this.value.slice(0, 14);
        });
    });

});
// 🔹 ABRIR / FECHAR SEÇÕES DO MENU
function toggleSection(id) {
    var section = document.getElementById(id);

    if (section) {
        if (section.style.display === "none") {
            section.style.display = "block";
        } else {
            section.style.display = "none";
        }
    }
}
// 🔹 ABRIR / FECHAR SEÇÕES COM SALVAMENTO
window.toggleSection = function(id) {
    var section = document.getElementById(id);

    if (section) {
        var aberto = section.style.display === "block";

        if (aberto) {
            section.style.display = "none";
            localStorage.setItem(id, "fechado");
        } else {
            section.style.display = "block";
            localStorage.setItem(id, "aberto");
        }
    }
};
// 🔹 RESTAURAR ESTADO AO CARREGAR
document.addEventListener("DOMContentLoaded", function () {
    ["tabelas", "cadastros"].forEach(function(id) {
        var estado = localStorage.getItem(id);
        var section = document.getElementById(id);

        if (section) {
            if (estado === "aberto") {
                section.style.display = "block";
            } else {
                section.style.display = "none";
            }
        }
    });
});
