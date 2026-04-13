// Função responsável por abrir/fechar a sidebar (menu lateral)
function toggleSidebar() {

    // Pega o elemento com id "sidebar"
    // e adiciona ou remove a classe "active"
    // Se tiver "active", remove → fecha
    // Se não tiver, adiciona → abre
    document.getElementById("sidebar").classList.toggle("active");
}


// Função para abrir/fechar um submenu específico
function toggleSubmenu(id) {

    // Pega o elemento do submenu com base no id recebido como parâmetro
    var menu = document.getElementById(id);

    // Adiciona ou remove a classe "open"
    // Isso normalmente controla a exibição via CSS (mostrar/esconder submenu)
    menu.classList.toggle("open");
}