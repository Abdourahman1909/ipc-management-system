document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-password-toggle]").forEach((toggle) => {
    const inputId = toggle.getAttribute("aria-controls");
    const input = document.getElementById(inputId);
    if (!input) return;

    toggle.addEventListener("click", () => {
      const willShow = input.type === "password";
      input.type = willShow ? "text" : "password";
      toggle.setAttribute("aria-pressed", String(willShow));
      toggle.setAttribute(
        "aria-label",
        willShow ? "Şifreyi gizle" : "Şifreyi göster"
      );
      toggle.querySelector("i").className = willShow
        ? "bi bi-eye-slash"
        : "bi bi-eye";
      input.focus({ preventScroll: true });
    });
  });
});
