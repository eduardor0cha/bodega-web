window.addEventListener("DOMContentLoaded", () => {
  document.getElementById("c-header__open-sidebar-button").addEventListener("click", () => {
    const sidebar = document.getElementById("c-sidebar");
    sidebar.classList.toggle("c-sidebar--isHidden");
  });

  document.getElementById("c-sidebar__close-sidebar-button").addEventListener("click", () => {
    const sidebar = document.getElementById("c-sidebar");
    sidebar.classList.toggle("c-sidebar--isHidden");
  });
});
