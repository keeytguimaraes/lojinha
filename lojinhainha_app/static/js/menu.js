function toggleSidebar() {
    document.getElementById("sidebar").classList.toggle("active");
}

function toggleSubmenu(id) {
    var menu = document.getElementById(id);
    menu.classList.toggle("open");
}