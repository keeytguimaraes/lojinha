document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("search-input");
    const tabela = document.getElementById("tabela-vendas");
    if (!input || !tabela) return;

    const linhas = Array.from(tabela.getElementsByTagName("tr")).slice(1);
    const sugestoesBox = document.getElementById("sugestoes-box");
    if (!sugestoesBox) return;

    // 🔹 estilo padrão (igual cliente)
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

        // 🔹 pega cliente + vendedor
        const resultados = linhas
            .map(linha => {
                const cliente = linha.getElementsByTagName("td")[1].textContent;
                const vendedor = linha.getElementsByTagName("td")[2].textContent;
                return { cliente, vendedor };
            })
            .filter(item =>
                item.cliente.toLowerCase().includes(termo) ||
                item.vendedor.toLowerCase().includes(termo)
            );

        resultados.forEach(item => {
            const div = document.createElement("div");
            div.textContent = item.cliente + " | " + item.vendedor;
            div.classList.add("item-sugestao");
            div.style.cursor = "pointer";
            div.style.padding = "5px 10px";

            div.addEventListener("click", function () {
                input.value = item.cliente; // pode trocar para vendedor se quiser
                sugestoesBox.innerHTML = "";
                sugestoesBox.style.display = "none";

                const linha = linhas.find(l => {
                    const cliente = l.getElementsByTagName("td")[1].textContent;
                    const vendedor = l.getElementsByTagName("td")[2].textContent;
                    return cliente === item.cliente && vendedor === item.vendedor;
                });

                if (linha) {
                    linha.scrollIntoView({ behavior: "smooth", block: "center" });
                    linha.style.backgroundColor = "#ffff99";
                    setTimeout(() => linha.style.backgroundColor = "", 1500);
                }
            });

            sugestoesBox.appendChild(div);
        });

        // 🔹 posicionamento (igual cliente)
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

    // 🔹 fechar ao clicar fora
    document.addEventListener("click", function (e) {
        if (e.target !== input && !sugestoesBox.contains(e.target)) {
            sugestoesBox.style.display = "none";
        }
    });
});