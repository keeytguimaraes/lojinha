document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("search-input");
    const tabela = document.getElementById("tabela-fornecedores");
    if (!input || !tabela) return;

    const linhas = Array.from(tabela.getElementsByTagName("tr")).slice(1);

    const sugestoesBox = document.getElementById("sugestoes-box");
    if (!sugestoesBox) return;

    input.addEventListener("input", function () {
        const termo = input.value.toLowerCase();
        sugestoesBox.innerHTML = "";

        if (!termo) return;

        const resultados = linhas
            .map(linha => linha.getElementsByTagName("td")[1].textContent)
            .filter(nome => nome.toLowerCase().includes(termo));

        resultados.forEach(nome => {
            const div = document.createElement("div");
            div.textContent = nome;
            div.classList.add("item-sugestao");
            div.style.cursor = "pointer";
            div.style.padding = "5px 10px";

            div.addEventListener("click", function () {
                input.value = nome;
                sugestoesBox.innerHTML = "";

                const linha = linhas.find(l => l.getElementsByTagName("td")[1].textContent === nome);
                if (linha) {
                    linha.scrollIntoView({ behavior: "smooth", block: "center" });
                    linha.style.backgroundColor = "#ffff99";
                    setTimeout(() => linha.style.backgroundColor = "", 1500);
                }
            });

            sugestoesBox.appendChild(div);
        });
    });
});