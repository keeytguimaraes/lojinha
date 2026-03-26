document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("search-input");
    const tabela = document.getElementById("tabela-clientes");
    if (!input || !tabela) return;

    const linhas = Array.from(tabela.getElementsByTagName("tr")).slice(1);

    let sugestoesBox = document.getElementById("sugestoes-box");
    if (!sugestoesBox) {
        sugestoesBox = document.createElement("div");
        sugestoesBox.id = "sugestoes-box";
        sugestoesBox.classList.add("lista-sugestoes");
        document.body.appendChild(sugestoesBox);
    }

    sugestoesBox.style.position = "absolute";
    sugestoesBox.style.background = "white";
    sugestoesBox.style.border = "1px solid #ccc";
    sugestoesBox.style.maxHeight = "150px";
    sugestoesBox.style.overflowY = "auto";
    sugestoesBox.style.display = "none";
    sugestoesBox.style.zIndex = "1000";

    input.addEventListener("input", function () {
        const termo = input.value.toLowerCase();
        sugestoesBox.innerHTML = "";

        if (!termo) {
            sugestoesBox.style.display = "none";
            return;
        }

        const resultados = linhas
            .map(linha => linha.getElementsByTagName("td")[1].textContent)
            .filter(nome => nome.toLowerCase().includes(termo));

        resultados.forEach(nome => {
            const div = document.createElement("div");
            div.textContent = nome;
            div.classList.add("item-sugestao");

            div.onclick = function () {
                input.value = nome;
                sugestoesBox.innerHTML = "";
                sugestoesBox.style.display = "none";

                const linha = linhas.find(l => l.getElementsByTagName("td")[1].textContent === nome);
                if (linha) {
                    linha.scrollIntoView({ behavior: "smooth", block: "center" });
                    linha.style.transition = "background 0.5s";
                    linha.style.backgroundColor = "#ffff99";
                    setTimeout(() => linha.style.backgroundColor = "", 1500);
                }
            };

            sugestoesBox.appendChild(div);
        });

        if (resultados.length > 0) {
            const rect = input.getBoundingClientRect();
            sugestoesBox.style.top = rect.bottom + window.scrollY + "px";
            sugestoesBox.style.left = rect.left + window.scrollX + "px";
            sugestoesBox.style.width = rect.width + "px";
            sugestoesBox.style.display = "block";
        } else {
            sugestoesBox.style.display = "none";
        }
    });

    document.addEventListener("click", function (e) {
        if (e.target !== input && !sugestoesBox.contains(e.target)) {
            sugestoesBox.style.display = "none";
        }
    });

    window.addEventListener("scroll", function () {
        if (sugestoesBox.style.display === "block") {
            const rect = input.getBoundingClientRect();
            sugestoesBox.style.top = rect.bottom + window.scrollY + "px";
            sugestoesBox.style.left = rect.left + window.scrollX + "px";
        }
    });
});