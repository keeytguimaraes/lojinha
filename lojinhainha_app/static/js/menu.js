// Função responsável por abrir/fechar a sidebar (menu lateral)
function toggleSidebar() {

    // Acessa o elemento HTML que possui o id "sidebar"
    // getElementById retorna exatamente um elemento da página com esse id
    var sidebar = document.getElementById("sidebar");

    // classList permite manipular as classes CSS do elemento
    // toggle("active") faz o seguinte:
    // - Se a classe "active" NÃO existir → ela é adicionada
    // - Se a classe "active" JÁ existir → ela é removida
    // Isso é muito usado para alternar estados (abrir/fechar menu)
    sidebar.classList.toggle("active");
}


// Função para abrir/fechar um submenu específico
function toggleSubmenu(id) {

    // Recebe um "id" como parâmetro (ou seja, o nome do submenu que será manipulado)
    // Busca no HTML o elemento correspondente a esse id
    var menu = document.getElementById(id);

    // classList.toggle("open") funciona como um interruptor:
    // - Adiciona a classe "open" se ela não existir
    // - Remove a classe "open" se ela já existir
    // Normalmente, no CSS, a classe "open" é usada para:
    // - Mostrar o submenu (ex: display: block)
    // - Ou aplicar animações de abertura
    menu.classList.toggle("open");
}