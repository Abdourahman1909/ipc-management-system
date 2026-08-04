/* ============================================================
   main.js — genel davranışlar (tüm sayfalarda yüklenir)
   1) Tarayıcı doğrulama mesajlarını TÜRKÇE'ye çevirir
   2) Flash mesajlarını toast olarak gösterir
   3) Form gönderiminde yükleme (loading) animasyonu ekler
   ============================================================ */

/* ---- 1) Türkçe doğrulama mesajları ---- */
document.addEventListener("invalid", function (e) {
  const el = e.target;
  if (!el.validity) return;
  if (el.validity.valueMissing) {
    el.setCustomValidity(el.tagName === "SELECT"
      ? "Lütfen listeden bir seçenek seçiniz."
      : "Bu alanın doldurulması zorunludur.");
  } else if (el.validity.patternMismatch) {
    el.setCustomValidity(el.dataset.formatMsg ||
      "Girilen değer istenen biçimde değil.");
  } else if (el.validity.typeMismatch && el.type === "email") {
    el.setCustomValidity("Geçerli bir e-posta adresi giriniz (örn. ad@example.com).");
  } else if (el.validity.tooShort) {
    el.setCustomValidity("En az " + el.minLength + " karakter girmelisiniz.");
  } else if (el.validity.rangeUnderflow) {
    el.setCustomValidity("Değer en az " + el.min + " olmalıdır.");
  } else {
    el.setCustomValidity("Girilen değer geçersiz.");
  }
}, true);

/* Kullanıcı yazmaya başlayınca özel mesajı temizle */
document.addEventListener("input", function (e) {
  if (e.target.setCustomValidity) e.target.setCustomValidity("");
}, true);
document.addEventListener("change", function (e) {
  if (e.target.setCustomValidity) e.target.setCustomValidity("");
}, true);

/* ---- 2) Toast bildirimleri ---- */
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".toast").forEach(function (t) {
    new bootstrap.Toast(t, { delay: 6000 }).show();
  });

  /* ---- 3) Şifre görünürlüğü ---- */
  document.querySelectorAll("[data-password-toggle]").forEach(function (toggle) {
    const input = document.getElementById(toggle.getAttribute("aria-controls"));
    const icon = toggle.querySelector("i");
    if (!input || !icon) return;

    function setVisibility(visible, returnFocus) {
      input.type = visible ? "text" : "password";
      toggle.setAttribute("aria-pressed", String(visible));
      toggle.setAttribute("aria-label", visible ? "Şifreyi gizle" : "Şifreyi göster");
      toggle.title = visible ? "Şifreyi gizle" : "Şifreyi göster";
      icon.className = visible ? "bi bi-eye-slash" : "bi bi-eye";
      if (returnFocus) input.focus({ preventScroll: true });
    }

    toggle.addEventListener("click", function () {
      setVisibility(input.type === "password", true);
    });

    const modal = toggle.closest(".modal");
    if (modal) {
      modal.addEventListener("hidden.bs.modal", function () {
        setVisibility(false, false);
      });
    }
  });

  /* ---- 4) Gönderim sırasında yükleme animasyonu ---- */
  document.querySelectorAll("form").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      if (!form.checkValidity()) return;   // geçersizse animasyon yok
      if (form.dataset.confirm && !window.confirm(form.dataset.confirm)) {
        event.preventDefault();
        return;
      }
      const btn = form.querySelector('button[type="submit"], button:not([type])');
      if (btn && !btn.dataset.noLoading) {
        btn.dataset.orjinal = btn.innerHTML;
        btn.innerHTML =
          '<span class="spinner-border me-2" role="status" aria-hidden="true"></span>İşleniyor…';
        btn.classList.add("disabled");
      }
    });
  });
});
