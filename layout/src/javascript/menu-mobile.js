const openMenu = document.querySelector("#open-menu");
const closeMenu = document.querySelector("#close-menu");
const menu = document.querySelector(".menu-hamburguer");
const backdrop = document.querySelector(".backdrop");

openMenu.addEventListener("click", () => {
    menu.classList.add("menu-active");
    backdrop.classList.add("active"); // Exibe o backdrop
});

closeMenu.addEventListener("click", () => {
    menu.classList.remove("menu-active");
    backdrop.classList.remove("active"); // Oculta o backdrop
});

// Adicionando a funcionalidade para fechar o menu ao clicar no backdrop
backdrop.addEventListener("click", () => {
    menu.classList.remove("menu-active");
    backdrop.classList.remove("active");
});
