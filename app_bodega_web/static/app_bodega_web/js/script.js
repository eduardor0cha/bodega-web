window.addEventListener("DOMContentLoaded", () => {
  document.getElementById("c-header__open-sidebar-button")?.addEventListener("click", () => {
    const sidebar = document.getElementById("c-sidebar");
    sidebar.classList.toggle("hidden");
  });

  document.getElementById("c-sidebar__close-sidebar-button")?.addEventListener("click", () => {
    const sidebar = document.getElementById("c-sidebar");
    sidebar.classList.toggle("hidden");
  });

  document.getElementById("c-account-menu__profile-pic")?.addEventListener("click", () => {
    const accountMenu = document.getElementById("c-account-menu__card");
    accountMenu.classList.toggle("hidden");
  });

  document.onclick = function (e) {
    if (!document.getElementById("c-account-menu__profile-pic")?.contains(e.target) && !document.getElementById("c-account-menu__card")?.contains(e.target)) {
      document.getElementById("c-account-menu__card")?.classList.add("hidden")
    };

    if (!document.getElementById("c-sidebar")?.contains(e.target) && !document.getElementById("c-header__open-sidebar-button")?.contains(e.target)) {
      document.getElementById("c-sidebar")?.classList.add("hidden")
    };
  };
});