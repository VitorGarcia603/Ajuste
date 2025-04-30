(() => {
  const KEY = "theme";
  const root = document.documentElement;
  const set  = t => { root.dataset.bsTheme = t; localStorage.setItem(KEY, t); };
  set(localStorage.getItem(KEY) || "light");
  document.addEventListener("click", e => {
    const btn = e.target.closest("[data-toggle-theme]");
    if (!btn) return;
    set(root.dataset.bsTheme === "light" ? "dark" : "light");
    btn.classList.toggle("bi-sun");
    btn.classList.toggle("bi-moon");
  });
})();
